import zmq
import sys
import time
import threading

class Node():

	def __init__(self, port):
		self.__context = None
		self.__socket = None
		self.__port = port
		#self.__host = None
		self.__message = 'None'

		self.__initConnection()

	def __initConnection(self):
		self.__context = zmq.Context()
		self.__socket = self.__context.socket(zmq.REP)
		print(self.__port, type(self.__port))
		self.__socket.bind("tcp://*:%s" % self.__port)

	def dwnldFile(self):

		while True:
			self.__message = self.__socket.recv_string()
			print ("Received request: ", self.__message)
			time.sleep (1)
			self.__socket.send_string("World from %s" % self.__port)


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

	node = Node(readInput())

	dwnldThread = threading.Thread(target = node.dwnldFile())
	dwnldThread.start()

	while True:
		print('still alive')

main()