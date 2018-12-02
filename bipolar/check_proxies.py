#!/usr/bin/env python

from bipolar import bipolar
from celery import group
from time import sleep
from elasticsearch import helpers, Elasticsearch
import sys
import json

ip_file = sys.argv[1]

ips = []
with open(ip_file) as f:
    ip_data = f.readlines()
    for data in ip_data:
        ip = data.strip().split(' ')[0]
        port = data.strip().split(' ')[1]
        ips.append((ip, port))

my_group1 = group([bipolar.proxy_check_socks.s(ip, port) for ip, port in ips])
group1_results = my_group1.apply_async()
while not group1_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
group1_results = group1_results.get()

output = []
for results in group1_results:
    if results is not None:
        for i in results:
            output.append(json.dumps(i))

print(output)

es = Elasticsearch(timeout=999999)
helpers.bulk(es, output, index='fnproxy', doc_type="doc")
