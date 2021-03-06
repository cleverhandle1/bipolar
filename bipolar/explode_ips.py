#!/usr/bin/env python
import bipolar
from celery import group
from time import sleep
from elasticsearch import helpers, Elasticsearch
import sys
import json

ip_net = sys.argv[1]

ips = bipolar.net_explode(ip_net)

for ip in ips:
    print(ip)

#group_results = my_group.apply_async()
#while not group_results.ready():
#    print('waiting for jobs to complete')
#    sleep(10)
#group_results = group_results.get()
#
#scan_data = {}
#for results in group_results:
#    ip = results['scan'].keys()[0]
#    scan_data[ip] = results['scan'][ip]
#
#output = []
#for ip in scan_data.keys():
#    open_ports = []
#    if 'tcp' in scan_data[ip].keys():
#        for port in scan_data[ip]['tcp'].keys():
#            state = scan_data[ip]['tcp'][port]['state']
#            if state == 'open':
#                open_ports.append(int(port))
#    output.append(json.dumps({'ip': ip, 'open_ports':open_ports}))
#
#try:
#    es = Elasticsearch(timeout=999999)
#    helpers.bulk(es, output, index='fnscan', doc_type="doc")
#except Exception as e:
#    print(e)
#    pass
#
#with open('data/output/scan_output.log', 'w') as f:
#    for out in output:
#        f.write(out + '\n')
#
