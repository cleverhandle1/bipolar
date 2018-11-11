#!/usr/bin/env python
import bipolar
from celery import group
from time import sleep
from elasticsearch import helpers, Elasticsearch
import sys
import json

sqli_file = sys.argv[1]

urls = []
with open(sqli_file) as f:
    url_data = f.readlines()
    for data in url_data:
        urls.append(data.strip())

my_group = group([bipolar.sqli_check.s(url) for url in urls])
group_results = my_group.apply_async()
print(group_results)
while not group_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
    group_results = group_results.get()

output = []
for results in group1_results:
    if results is not None:
        for i in results:
            output.append(json.dumps(i))

print(output)

es = Elasticsearch(timeout=999999)
helpers.bulk(es, output, index='fnsqli', doc_type="doc")
