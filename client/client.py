import zmq
import sys
import time


port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)

#  Do request, waiting for a response

print ("Waiting request... Choose 1-Upload 2-Show 3-Download")

read = input()
#time.sleep(1)
while(read != "1" and read != "2" and read != "3"):
    print ("please, Choose 1-Upload 2-Show 3-Download")
    read = input()
    
if(read=="1"):
    socket.send_string(read)
    print ("Sending request...")
    time.sleep(1)
 

#  Get the port.
message = socket.recv_string()
time.sleep(1)
print ("Received port ", message)

##################################################################
#connect to process with given port and upload file

socket1 = context.socket(zmq.REQ)
socket1.connect ("tcp://localhost:%s" % message)

print ("connecting to process...Enter your file") 
file=input()

f = open(file,'rb')
print ('Sending...')
l = f.read()
socket1.send(l)
time.sleep(1)
f.close()
#print ("Done Sending")

print (socket1.recv_string())
time.sleep(1)
socket1.send_string("Done Receiving")
time.sleep(1)
socket1.close()