from multiprocessing import Process, Manager
from Nodes_client import main as nodeMain
from 

if __name__ == '__main__':
	node1 = Process(target = nodeMain, args = (sys.argv[0], "2001", "2002", "2003", "2004", "2005"))
	node1.start()

	node2 = Process(target = nodeMain, args = (sys.argv[0], "2011", "2012", "2013", "2014", "2015"))
	node2.start()
	
	node3 = Process(target = nodeMain, args = (sys.argv[0], "2021", "2022", "2023", "2024", "2025"))
	node3.start()

	# replicate = Process(target = )


	node1.join()
	node2.join()
	node3.join()