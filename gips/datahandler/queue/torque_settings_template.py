TASK_QUEUE    = 'torque'
# path to the correct python binary on the worker node
REMOTE_PYTHON = '/usr/bin/env python'
# named queue to which jobs should be submitted
TORQUE_QUEUE  = '$QUEUE_NAME'
# prints out the generated torque jobs; may enable more debugging in the future
DH_DEBUG = True
# see nodes entry in:
# http://docs.adaptivecomputing.com/torque/4-0-2/Content/topics/2-jobs/requestingRes.htm
#TORQUE_NODE  = 'specific-node-du-jour'
# place to put torque job output files
TORQUE_OUTPUT = '$TORQUE_OUTPUT'