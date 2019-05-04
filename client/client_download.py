#threading is used to distribute file requests over multiple threads, each requesting a portion of the file
#use another additional thread to perform time out, handling of preocesses dying
import zmq
import sys
import time
import threading


class Client():

	def __init__(self, port):
		
		#for master connection
		self.__context = None
		self.__socket = None
		self.__port = port
		#self.__host = None
		self.__message = None

		#for download
		self.__state = None
		self.__fileName = None
		self.__fileSize = None
		self.__ips = None
		self.__dataPorts = None
		self.__dataSocket = None

		self.__initConnectionMaster()

	def __initConnectionMaster(self):
		self.__context = zmq.Context()
		self.__socket = self.__context.socket(zmq.REQ)
		print(self.__port, type(self.__port))
		self.__socket.connect("tcp://localhost:%s" % self.__port)

	def __initConnectionNodes(self):

		self.__dataSocket = self.__context.socket(zmq.REQ)
		for i in range(len(self.__ips)):
			self.__dataSocket.connect("tcp://" + self.__ips[i] + ":" + self.__dataPorts[i])

	def reqDwnld(self, fileName):

		self.__fileName = fileName

		print("Sending request for download ...")
		self.__socket.send_string("REQ_DWNLD " + fileName)
		self.__message = self.__socket.recv_string()
		print("Received list of nodes to download from and file size")

		self.__message = self.__message.split()
		self.__state = self.__message[0]
		self.__fileSize = int(self.__message[1])
		self.__ips = self.__message[2:2+int((len(self.__message)-2)/2)]
		self.__dataPorts = self.__message[2+int((len(self.__message)-2)/2):]

		#print(fileSize, ports)

	def dwnldFile(self):

		received = 0
		shard = 1

		self.__initConnectionNodes()

		while received < self.__fileSize:

			print("Sending request for shard ", shard, "...")
			self.__dataSocket.send_string(self.__fileName + " " + str(shard))
			self.__message = self.__dataSocket.recv_string()
			print("Received reply ", "[", self.__message, "]")
			received += 1024
			shard += 1


def readPort():
	port = sys.argv[1]
	int(port)
	return port

#def readHost():
	#host = sys.argv[2]
	#return host

def readInput():
	return readPort()#, readHost()

def main():

	fileName = "small.mp4"

	client = Client(readInput())
	client.reqDwnld(fileName)
	client.dwnldFile()

main()