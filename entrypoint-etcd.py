#!/usr/bin/env python3
import etcd
import os
import sys
import subprocess
import time
print('Connecting to etcd')

is_ready = False
client = etcd.Client(host='etcd', port=2379, allow_reconnect=True, read_timeout=5)

print('Connected to etcd')

while not is_ready:
    print('is_ready = ', is_ready)
    print('Trying to talk to etcd')

    try:
        print('Reading PG user')
        os.environ['POSTGRES_USER'] = client.read('/db_data/user').value
        print('Reading PG db')
        os.environ['POSTGRES_DB'] = client.read('/db_data/name').value
        print('Reading PG pass')
        os.environ['POSTGRES_PASSWORD'] = client.read('/db_data/pswd').value
        print('Read all data')
        is_ready = True
        print('is_ready set to true')

    except etcd.EtcdException as e:
        print('Can\'t talk to etcd')
        print(e)
        print('Error printed')
        is_ready = False
        print('is_ready set to false')
        time.sleep(5)

    print('After try')

print(is_ready)
print('About to run elo')
sys.stdout.flush()
if is_ready:
    print('Running elo')
    sys.stdout.flush()
    subprocess.run(('python3', '/usr/local/bin/elo.py', *sys.argv[1:]), stdin=sys.stdin, stdout=sys.stdout)
