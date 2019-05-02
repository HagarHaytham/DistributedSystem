#!/bin/sh

python shard.py 5000 &
python shard.py 5001 &
python shard.py 5002 &

python shard.py 5005 &
python shard.py 5006 &
python shard.py 5007 &

python shard.py 5010 &
python shard.py 5011 &
python shard.py 5012 &

python clientdb.py 