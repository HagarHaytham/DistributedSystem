#!/bin/sh

python shardsys.py 5000 5030 5035 5045 3000 &

python shardsys.py 5005 5035 5030 5045 3001 &

python shardsys.py 5010 5045 5030 5035 3002 &

python clientdb.py 


#awl 25 ports for server-client connection w tany 25 for dataNode-server connection
#1 for db
#2, 3, 4 for 1st data node machine
#5, 6, 7 for 2nd data node machine
#8, 9, 10 for 2nd data node machine
#11 for alive receive

#python server.py 3000 2001 2002 2003 2004 2005 2006 2007 2008 2009 2010 

# cd Nodes
# python Nodes_client.py 2001 2051 2101 ipserverSuccess