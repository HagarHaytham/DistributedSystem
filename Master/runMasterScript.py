
import sys
from multiprocessing import Process, Manager
from server import main as serverMain
from replicates import main as repMain


if __name__ == '__main__':

	manager = Manager()
	lookupTable = manager.dict()
	Nports = manager.list()
	files = manager.list()

	lookupTable[0] = [{'':[]}, 'A']
	lookupTable[1] = [{'':[]}, 'A']
	lookupTable[2] = [{'':[]}, 'A']
	files = []	
	seed = 2001
	defSeed = 2001

	for i in range(3):
		temp = []
		for j in range(3):
			#[0] = ip of machine
			#[1] = alive port between node and server
			#[2] = upload port between node and client
			#[3] = success port between node and server
			#[4] = download port between node and client
			#[5] = replicate port between node and server
			#[6] = replicate port between node and node
			temp.append([sys.argv[i+1], "2001", str(seed + 1), str(seed + 2), str(seed + 3), str(defSeed + 4), str(defSeed + 5), 'A', 'A'])
			#shift by 10 for 2nd process
			seed = seed + 10

		defSeed = defSeed + 10

		Nports.append(temp)

	sPort = [["2005",'A'], ["2015",'A'], ["2025",'A']]
	nPort = [["2006",'A'], ["2016",'A'], ["2026",'A']]


	print(Nports)
	#Nports = [[[''], [], []], [[], [], []], [[], [], []]]
	master1 = Process(target = serverMain, args = (lookupTable, Nports, files, "3000"))
	master1.start()
	
	master2 = Process(target = serverMain, args = (lookupTable, Nports, files, "3100"))
	master2.start()
	
	master3 = Process(target = serverMain, args = (lookupTable, Nports, files, "3200"))
	master3.start()

	replication= Process(target = repMain, args = (lookupTable, files,nPort, sPort))
	replication.start()
    
	master1.join()
	master2.join()
	master3.join()
	replication.join()