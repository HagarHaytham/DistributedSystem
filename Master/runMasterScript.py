from multiprocessing import Process, Manager
from server import main as serverMain

if __name__ == '__main__':

	manager = Manager()
	lookupTable = manager.dict()
	Nports = manager.list()

	lookupTable[0] = [{'':[]}, 'A']
	lookupTable[1] = [{'':[]}, 'A']
	lookupTable[2] = [{'':[]}, 'A']
	
	seed = 2001

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
			temp.append([sys.argv[i+1], str(seed), str(seed + 1), str(seed + 2), str(seed + 3), str(seed + 4), str(seed + 5), 'A', 'A'])
			#shift by 10 for 2nd process
			seed = seed + 10

		Nports.append(temp)


	print(Nports)
	#Nports = [[[''], [], []], [[], [], []], [[], [], []]]
	master1 = Process(target = serverMain, args = (lookupTable, Nports, "3000"))
	master1.start()
	
	master2 = Process(target = serverMain, args = (lookupTable, Nports, "3100"))
	master2.start()
	
	master3 = Process(target = serverMain, args = (lookupTable, Nports, "3200"))
	master3.start()


	master1.join()
	master2.join()
	master3.join()