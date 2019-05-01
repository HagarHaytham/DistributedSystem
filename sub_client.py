import sys
import zmq
import socket

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)
    
if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

#####MASTERRRRR#############


# Socket to talk to server
context = zmq.Context()
socket1 = context.socket(zmq.SUB)

print("Collecting updates from weather server...")
socket1.connect ("tcp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket1.connect ("tcp://localhost:%s" % port1)


# Subscribe to zipcode, default is NYC, 10001
#messagedata = socket1.gethostbyname(socket.gethostname())
#messagedata+= " " + port
socket1.setsockopt_string(zmq.SUBSCRIBE, "ALIVE")

# Process 5 updates
total_value = 0
while(1):
    string = socket1.recv()
    topic, IP = string.split()
    #total_value += int(messagedata)
    print (topic, IP)

#print ("Average messagedata value for topic '%s' was %dF" % (topicfilter, total_value / update_nbr))
      


