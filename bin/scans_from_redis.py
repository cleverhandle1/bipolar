#!/usr/bin/env python
from elasticsearch import helpers, Elasticsearch
import json
import redis
import os

r = redis.StrictRedis(password=os.environ['REDIS_PASS'])

keys = []
for key in r.keys('*'):
        try:
            keys.append(json.loads(r.get(key)))
        except Exception as e:
            print(e)

scans = []
for k in keys:
    try:
        if 'result' in k.keys():
            if 'scan' in k['result'].keys():
                scans.append(k['result'])
    except Exception as e:
        print e
        pass

scan_data = {}
for results in scans:
    ip = results['scan'].keys()[0]
    scan_data[ip] = results['scan'][ip]

output = []
for ip in scan_data.keys():
    open_ports = []
    if 'tcp' in scan_data[ip].keys():
        for port in scan_data[ip]['tcp'].keys():
            state = scan_data[ip]['tcp'][port]['state']
            if state == 'open':
                open_ports.append(int(port))
    output.append(json.dumps({'ip': ip, 'open_ports':open_ports}))

print output

es = Elasticsearch(timeout=999999)
result = helpers.bulk(es, output, index='fnscan', doc_type="doc")
print result
