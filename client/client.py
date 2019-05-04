import zmq
import sys
import time
import threading

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 =  sys.argv[2]
    int(port1)

#connect to server
context = zmq.Context()
print ("Connecting to server...")
socket = context.socket(zmq.REQ)
socket.connect ("tcp://localhost:%s" % port)
if len(sys.argv) > 2:
    socket.connect ("tcp://localhost:%s" % port1)


def success():
    while 1:
        #connect to server to recieve success uploading
        socketServer = context.socket(zmq.REP)
        portx = "1088"
        socketServer.bind ("tcp://*:%s" % portx)
        #recieving success from server
        print(socketServer.recv_string())
    
t1 = threading.Thread(target=success) 

t1.start()
    
while 1:
   
   
    ##################################################################

    #  Do request, waiting for a response
    print ("Waiting request... Choose 1-Upload 2-Show 3-Download")
    read = input()
    
    #send the choice to server    
    socket.send_string(read)
    print ("Sending request...")
      
    ##################################################################
    #connect to node/process with given port to upload file
    socket1 = context.socket(zmq.REQ)
    socket1.connect ("tcp://localhost:%s" % "2000")
  
    if(read == '1'):
     #  Get the port from server
        message = socket.recv_string()
        print ("Received port ", message)
        #uploading happens
        print ("connecting to process...Enter your file") 
        #reading video
        file=input()
        f = open(file,'rb')
        print ('Sending...')
        l = f.read()
        #sending video
        socket1.send(l)
        f.close()
        print ("Done Sending")
        #recieve complete
        print (socket1.recv_string())
        #sending file name
        socket1.send_string(file)
        
        
        
    elif(read == "2"):
        
        #show happening
        print ("connecting to process...")
        print(socket.recv_string())
        #recieving success from server
        #print(socket.recv_string())
        
    #socket1.close()