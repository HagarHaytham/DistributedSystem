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
#send the option to server    
socket.send_string(read)
print ("Sending request...")

#  Get the port from server
message = socket.recv_string()

print ("Received port ", message)

##################################################################
#connect to node/process with given port to upload file

socket1 = context.socket(zmq.REQ)
socket1.connect ("tcp://localhost:%s" % "2000")


##################################################################
#connect to server to recieve success uploading
socketServer = context.socket(zmq.REP)
portx = "1088"
socketServer.bind ("tcp://*:%s" % portx)

##################################################################
#uploading happens

print ("connecting to process...Enter your file") 
file=input()

f = open(file,'rb')
print ('Sending...')
l = f.read()
#sending video
socket1.send(l)

f.close()
print ("Done Sending")
#recieve complete
print (socket1.recv())
#sending file name
socket1.send_string(file)
time.sleep(1)
#recieving success from server
print(socketServer.recv_string())

#socket1.close()