import zmq
import sys
import time
import threading
import ClientF as c
from multiprocessing import process


#connect to default port of server from db, connect to this port w send username
def initConnServer(context, serverPort,ipServer):
    
    socketID = context.socket(zmq.REQ)
    socketID.connect ("tcp://%s:%s" % (ipServer,serverPort))
    
    return socketID


#send choice of client to default port of server from db
def sendChoice(socketID,choice):
    socketID.send_string(choice)
    return socketID.recv_string()


def initUplNodePort(context,dataNodePort,dataIps):
    #send,recv from datanode port from server
    dataNodeSocket = context.socket(zmq.REQ)
    for i in range (len(dataIps)):
        dataNodeSocket.connect ("tcp://%s:%s" % (dataIps[i],dataNodePort))
    return dataNodeSocket


def initDwnldNodePort(msg):
    return


def closeDwnld(dataNodeSockets):
    return


def success(successSocket):
    successSocket.send_string('s')
    print(successSocket.recv_string())
    return


def main(IPS,ipServer,dataIps):

    context = zmq.Context()

    #connect to db get user ID
    # IPS = ['localhost','localhost','localhost'] # 3 shards IPs
    # for testing on one machine , can begin from the same port in diffrent machines
    # portsbegin = [5000,5005,5010] # shard 1 begins from port 5000 , shard 2 begins from 5005 and shard 3 from 5010     
    isAuthenticated, serverPort = c.UserAuthenticate(IPS)
    
    print(isAuthenticated, serverPort)
    #if connected to db true
    
    if isAuthenticated:
        ##################################################################
        #initialize connection with server and send userName
        print("enter auth")
        socketID = initConnServer(context, serverPort,ipServer)
        
        while 1:
            ##################################################################
            #  Do request, waiting for a response
            print ("Waiting request... Choose 1-Upload 2-Show 3-Download")
            read = input()
            reply = sendChoice(socketID,read)
            print(reply)
            ##################################################################
           
            if(read == '1'):
             #  Get the port from server
                dataNodeSocket = initUplNodePort(context,reply,dataIps)

                #uploading happens
                print ("connecting to process...Enter your file") 

                #reading video
                file = input()
                f = open(file,'rb')
                print('Sending...')

                #sending file name
                dataNodeSocket.send_string(file)

                #dummy receive
                print (dataNodeSocket.recv_string())
                
                l = f.read()
                f.close()
                #sending video
                dataNodeSocket.send(l)
                dataNodeSocket.recv_string()
                dataNodeSocket.close()
                
                print ("Done Sending,waiting for success")
                success(socketID)
                
                
            elif(read == "2"):
                
                files = socketID.recv_string()
                print(files)

            elif(read == "3"):

                #download happening
                msg = reqSocket.recv_string()
                reqSocket.close()
                dataNodeSockets = initDwnldNodePort(msg)
                closeDwnld(dataNodeSockets)
                print ("connecting to process...")
    return 

if __name__=='__main__':
    IPS=[]
    for i in range(3):
        IPS.append(sys.argv[i+1])
    IPserver = sys.argv[4]
    IPSdata =[]
    for i in range (5,8):
        IPSdata.append(sys.argv[i])
    main(IPS,IPserver,IPSdata)