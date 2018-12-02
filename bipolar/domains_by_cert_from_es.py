#!/usr/bin/env python
import sys
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

es = Elasticsearch()

s = Search(using=es, index="celery")
s = s.query("query_string", query='subjectAltName', analyze_wildcard=True)

response = s.scan()

domains = set()
for res in response:
    json_res = json.loads(res.result)
    for key in json_res['result']['subjectAltName']:
        domains.add(key[1].replace('*.',''))

for domain in domains:
    print(domain)
