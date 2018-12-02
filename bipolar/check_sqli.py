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
for child in group_results.children:
    print(child.as_tuple()[0][0])
