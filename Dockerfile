FROM postgres:11-alpine
RUN apk add --no-cache python3
RUN pip3 install python-etcd
COPY entrypoint-etcd.py /usr/local/bin/
ENTRYPOINT ["/usr/bin/python3", "/usr/local/bin/entrypoint-etcd.py"]
