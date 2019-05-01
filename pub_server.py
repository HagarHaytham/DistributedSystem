import zmq
import random
import sys
import time
import socket
#####NOOOOOODES#############

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket1 = context.socket(zmq.PUB)
socket1.bind("tcp://*:%s" % port)

topicfilter = socket.gethostbyname(socket.gethostname())
topicfilter+= "@" + port


while True:
    #topic = random.randrange(9999,10005)
    messagedata = "ALIVE"
    #print ("%s %s" % (messagedata, topicfilter))
    socket1.send_string("%s %s" % (messagedata, topicfilter))
    time.sleep(1)
