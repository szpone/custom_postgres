#!/usr/bin/python3
import etcd
import os
import sys
from secrets import choice
from string import ascii_letters, digits

pswd  = ascii_letters + digits
secret_key = ''.join(choice(pswd) for i in range(20))
db_password = ''.join(choice(pswd) for i in range(20))

setup_completed = False
client = etcd.Client(host='etcd', port=2379, allow_reconnect=True)

while not setup_completed:

    try:
        client.read('/setup_completed')
        setup_completed = True
    except etcd.EtcdKeyNotFound:
        client.write('/django', secret_key)
        client.write('/db_data/user', 'admin')
        client.write('/db_data/name', 'baza')
        client.write('/db_data/pswd', db_password)
        client.write('/setup_completed', 1)

os.environ['POSTGRES_USER'] = client.read('/db_data/user').value
os.environ['POSTGRES_DB'] = client.read('/db_data/name').value
os.environ['POSTGRES_PASSWORD'] = client.read('/db_data/pswd').value

os.execvp('docker-entrypoint.sh', ('docker-entrypoint.sh', *sys.argv[1:]))