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


def initDwnldNodePorts(context, dwnldPorts):
    dwnldPorts = dwnldPorts.split()
    state = dwnldPorts[0]
    fileSize = int(dwnldPorts[1])
    ips = dwnldPorts[2:2+int((len(dwnldPorts)-2)/2)]
    dataPorts = dwnldPorts[2+int((len(dwnldPorts)-2)/2):]

    if(state == 'Found'):
        dwnldSocket = context.socket(zmq.REQ)
        for i in range(len(ips)):
            dwnldSocket.connect("tcp://" + ips[i] + ":" + dataPorts[i])

        dwnld(context, fileSize, ips, dwnldSocket)
    return

def dwnld(context, fileSize, ips, dwnldSocket):
    received = 0
    shard = 1

    while received < fileSize:

        print("Sending request for shard ", shard, "...")
        dwnldSocket.send_string(str(shard))
        message = dwnldSocket.recv_string()
        print("Received reply ", "[", message, "]")
        received += 1024
        shard += 1

    closeDwnld(dwnldSocket)
    return


def closeDwnld(dwnldSocket):
    dwnldSocket.close()
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
                socketID.send_string("dummy")
                reply = socketID.recv_string()

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
                print(socketID.recv_string())
                socketID.send_string("dummy")
                # dwnldPorts = socketID.recv_string()
                # initDwnldNodePorts(context, dwnldPorts)
                # print(dwnldPorts)

            elif(read == "3"):

                #download happening
                print('enter file name')
                socketID.send_string(input())
                dwnldPorts = socketID.recv_string()
                initDwnldNodePorts(context, dwnldPorts)

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