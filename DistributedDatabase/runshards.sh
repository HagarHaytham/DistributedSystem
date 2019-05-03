#!/bin/sh

python shard.py 5000 5005 5010 &
python shard.py 5001 5005 5010 &
python shard.py 5002 5005 5010 &

python shard.py 5005 5000 5010 &
python shard.py 5006 5000 5010 &
python shard.py 5007 5000 5010 &

python shard.py 5010 5000 5005 &
python shard.py 5011 5000 5005 &
python shard.py 5012 5000 5005 &

python clientdb.py 