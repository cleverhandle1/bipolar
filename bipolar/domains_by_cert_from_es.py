#!/usr/bin/env python
import sys
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

start = sys.argv[1]
end = sys.argv[2]

es = Elasticsearch('192.168.0.69')

s = Search(using=es, index="celery")
s = s.query("query_string", query='subjectAltName', analyze_wildcard=True)
s = s.filter('range', ** {'@timestamp': {'gte': start, 'lt': end}})


response = s.scan()

domains = set()
for res in response:
    json_res = json.loads(res.result)
    for key in json_res['result']['subjectAltName']:
        domains.add(key[1].replace('*.',''))

for domain in domains:
    print(domain)
