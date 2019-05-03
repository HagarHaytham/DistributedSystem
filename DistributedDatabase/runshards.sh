#!/bin/sh

python shard.py 5000 5030 5035 5040 &
python shard.py 5001 5031 5035 5040 &
python shard.py 5002 5032 5035 5040 &

python shard.py 5005 5035 5030 5040 &
python shard.py 5006 5036 5030 5040 &
python shard.py 5007 5037 5030 5040 &

python shard.py 5010 5040 5030 5035 &
python shard.py 5011 5041 5030 5035 &
python shard.py 5012 5042 5030 5035 &

python clientdb.py 