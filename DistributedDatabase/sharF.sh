#!/bin/sh

python shardF.py 192.168.1.10 192.168.1.8

python clientF.py 3 192.168.1.8 192.168.1.9 192.168.1.10