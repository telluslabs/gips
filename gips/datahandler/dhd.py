#!/usr/bin/env python

import argparse
import logging
import logging.handlers
import logging.config
from multiprocessing import Process
import os
import pickle
from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import socket
import SocketServer
import struct

from gips import utils
from gips.datahandler import api as dh_api


class ThreadedRPC(SocketServer.ThreadingMixIn, SimpleXMLRPCServer):
    pass

class RequestHandler (SimpleXMLRPCRequestHandler):
    pass


class LogRecordStreamHandler (SocketServer.StreamRequestHandler):
    """Handler for a streaming logging request.

    This basically logs the record using whatever logging policy is
    configured locally.
    """

    def handle (self):
        """
        Handle multiple requests - each expected to be a 4-byte length,
        followed by the LogRecord in pickle format. Logs the record
        according to whatever policy is configured locally.
        """
        while True:
            chunk = self.connection.recv(4)
            if len(chunk) < 4:
                break
            slen = struct.unpack('>L', chunk)[0]
            chunk = self.connection.recv(slen)
            while len(chunk) < slen:
                chunk = chunk + self.connection.recv(slen - len(chunk))
            obj = self.unPickle(chunk)
            record = logging.makeLogRecord(obj)
            self.handleLogRecord(record)

    def unPickle (self, data):
        return pickle.loads(data)

    def handleLogRecord (self, record):
        # if a name is specified, we use the named logger rather than the one
        # implied by the record.
        if self.server.logname is not None:
            name = self.server.logname
        else:
            name = record.name
        logger = logging.getLogger(name)
        # N.B. EVERY record gets logged. This is because Logger.handle
        # is normally called AFTER logger-level filtering. If you want
        # to do filtering, do it at the client end to save wasting
        # cycles and network bandwidth!
        logger.handle(record)


class LogRecordSocketReceiver (SocketServer.ThreadingTCPServer):
    """
    Simple TCP socket-based logging receiver suitable for testing.
    """

    allow_reuse_address = 1

    def __init__ (self, host='localhost',
                 port=logging.handlers.DEFAULT_TCP_LOGGING_PORT,
                 handler=LogRecordStreamHandler):
        SocketServer.ThreadingTCPServer.__init__(self, (host, port), handler)
        self.abort = 0
        self.timeout = 1
        self.logname = None

    def serve_until_stopped (self):
        import select
        abort = 0
        while not abort:
            rd, wr, ex = select.select([self.socket.fileno()],
                                       [], [],
                                       self.timeout)
            if rd:
                self.handle_request()
            abort = self.abort

_default_server_logging = {
    'version': 1,
    'formatters': {
        'dhdformatter': {
            'format': '%(levelname)s %(asctime)s --- %(dh_id)s:%(filename)s:%(funcName)s\n'
                      '%(message)s\n'
                      '--------------------------------------------------------',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'dhdformatter',
        },
    },
    'root': {'handlers': ['console']},
}

def serve_log (host, port):
    """Configure and run the logging server portion of dhd.

    Part of the contract for passing log records to this server is to
    provide a 'dh_id' attrib in LogRecords passed in, which must be
    usefully convertible to a string.  It should identify the running
    code that emitted the LogRecord, such as a job ID, process ID, or
    similar.
    """
    # not using basicConfig because setting the log level mysteriously didn't work
    logging_config = utils.get_setting('SERVER_LOGGING', _default_server_logging)
    logging.config.dictConfig(logging_config)
    tcpserver = LogRecordSocketReceiver(host, port)
    tcpserver.serve_until_stopped()

def serve_xmlrpc (host, port):
    utils.configure_logging()
    #server = SimpleXMLRPCServer(
    server = ThreadedRPC(
        (host, port),
        requestHandler=RequestHandler,
        allow_none=True,
    )
    server.register_introspection_functions()

    server.register_function(dh_api.get_catalog)
    server.register_function(dh_api.submit_request)
    server.register_function(dh_api.get_status)
    server.register_function(dh_api.get_results)

    server.serve_forever()

    
def main ():
    parser = argparse.ArgumentParser(prog=os.path.split(__file__)[1],
                                     description='Geokit daemon')

    parser.add_argument('--host', help='hostname or address',
                        default=utils.settings().GEOKIT_SERVER)
    parser.add_argument('--logport', help='port for log server',
                        default=utils.settings().LOG_PORT)
    parser.add_argument('-l', '--logfile', help='logfile',
                        default='geokitd.log')
    parser.add_argument('--xmlrpcport', help='port for xmlrpc server',
                        default=utils.settings().XMLRPC_PORT)

    args = parser.parse_args()

    p = Process(target=serve_log, args=(args.host, args.logport))
    p.start()

    p = Process(target=serve_xmlrpc, args=(args.host, args.xmlrpcport))
    p.start()

    
if __name__ == '__main__':
    main()
    

