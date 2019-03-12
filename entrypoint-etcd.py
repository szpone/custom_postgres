#!/usr/bin/python3
import etcd
import os
import sys
from secrets import choice
from string import ascii_letters, digits

alphabet = ascii_letters + digits

secret_key = ''.join(choice(alphabet) for i in range(20))
db_name = ''.join(choice(alphabet) for i in range(20))
db_user = ''.join(choice(alphabet) for i in range(20))
db_password = ''.join(choice(alphabet) for i in range(20))

setup_completed = False
is_ready = False
client = etcd.Client(host='etcd', port=2379, allow_reconnect=True)

try:
    client.read('/setup_completed')
    setup_completed = True
except etcd.EtcdKeyNotFound:
    setup_completed = False
    client.write('/django', secret_key)
    client.write('/db_data/user', db_user)
    client.write('/db_data/name', db_name)
    client.write('/db_data/pswd', db_password)
    client.write('/setup_completed', 1)



if setup_completed:

    while not is_ready:
        try:
            os.environ['POSTGRES_USER'] = client.read('/db_data/user').value
            os.environ['POSTGRES_DB'] = client.read('/db_data/name').value
            os.environ['POSTGRES_PASSWORD'] = client.read('/db_data/pswd').value
            is_ready = True
        except etcd.EtcdKeyNotFound:
            is_ready = False

if is_ready:
    os.execvp('docker-entrypoint.sh', ('docker-entrypoint.sh', *sys.argv[1:]))
