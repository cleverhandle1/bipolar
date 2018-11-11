#!/usr/bin/env python
import bipolar
from celery import group
from time import sleep
from elasticsearch import helpers, Elasticsearch
import sys
import json

ip_file = sys.argv[1]

urls = []
with open(ip_file) as f:
    ip_data = f.readlines()
    for ip in ip_data:
        urls.append('http://' + ip.strip())

my_group1 = group([bipolar.http_get.s(url) for url in urls])
group1_results = my_group1.apply_async()
while not group1_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
group1_results = group1_results.get()

output = []
for results in group1_results:
    if results is not None:
        output.append(json.loads(results))

print(output)

es = Elasticsearch(timeout=999999)
helpers.bulk(es, output, index='fnhttp', doc_type="doc")

