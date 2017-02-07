#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import socket

from gips.datahandler import geokit_api

class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

server = SimpleXMLRPCServer(
    # TODO: should be able to use socket.fqdn() but
    #       doesn't return a fqdn on schedtst
    ('schedtst.ags.io', 8000),
    requestHandler=RequestHandler,
    allow_none=True,
)
server.register_introspection_functions()

server.register_function(geokit_api.get_datacatalog)
server.register_function(geokit_api.submit_job)
server.register_function(geokit_api.job_status)
server.register_function(geokit_api.stats_request_results)
server.register_function(geokit_api.stats_request_results_filter)

server.serve_forever()
