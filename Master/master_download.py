#Add file size to lookup table
import zmq
import sys
import time
import threading

class Server():

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


	#TODO add search in lookup table
	def __getDwnldList(self, fileName):
		return "localhost localhost", "6666 8888"

	def dwnldFile(self, fileName):

		while True:
			self.__message = self.__socket.recv_string()
			print ("Received request: ", self.__message)
			time.sleep (1)
			state = "Found"		#retrieve from lookup table
			fileSize = "3000"	#retrieve from lookup table

			#retrieve list of ips and ports from lookup table
			ips, ports = self.__getDwnldList(fileName)
			
			self.__socket.send_string(state + " " + fileSize + " "+ ips + " " + ports)


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

	server = Server(readInput())

	dwnldThread = threading.Thread(target = server.dwnldFile("dump.txt"))
	dwnldThread.start()

	while True:
		print('still alive')

main()