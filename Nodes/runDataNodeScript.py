from multiprocessing import Process, Manager

from Nodes_client import main as nodeMain

if __name__ == '__main__':
	node1 = Process(target = nodeMain, args = ("2001", "2002", "2003", "2004", "2005"))
	node2 = Process(target = nodeMain, args = ("2011", "2012", "2013", "2014", "2015"))
	node3 = Process(target = nodeMain, args = ("2021", "2022", "2023", "2024", "2025"))

	node1.start()
	node2.start()
	node3.start()

	node1.join()
	node2.join()
	node3.join()