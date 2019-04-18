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
#while(read.find("Upload") == -1):
#    print ("Choose 'Upload' or 'show'")
#    read = input()
    
socket.send_string(read)
print ("Sending request...")
#time.sleep (1) 

#  Get the port.
message = socket.recv_string()

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

f.close()
print ("Done Sending")

print (socket1.recv())
#sending file name
socket1.send_string(file)
#recieving success from srver
print(socket.recv_string())
#socket1.close()