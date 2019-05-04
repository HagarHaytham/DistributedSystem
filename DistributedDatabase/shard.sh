#!/bin/sh

python shardsys.py 5000 5030 5035 5045 &

python shardsys.py 5005 5035 5030 5045 &

python shardsys.py 5010 5045 5030 5035 &

python clientdb.py 