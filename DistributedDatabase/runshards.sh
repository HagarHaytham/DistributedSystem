#!/bin/sh

python shard.py 5000 5030 5035 5045 &
python shard.py 5001 5031 5035 5045 &
python shard.py 5002 5032 5035 5045 &

python shard.py 5005 5035 5030 5045 &
python shard.py 5006 5036 5030 5045 &
python shard.py 5007 5037 5030 5045 &

python shard.py 5010 5045 5030 5035 &
python shard.py 5011 5046 5030 5035 &
python shard.py 5012 5047 5030 5035 &

python clientdb.py 