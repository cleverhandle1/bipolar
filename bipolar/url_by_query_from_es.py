#!/usr/bin/env python
import json
import sys
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import QueryString
from elasticsearch import Elasticsearch

query = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]

es = Elasticsearch('192.168.0.69')

s = Search(using=es, index="celery") 
s = s.query("query_string", query=query, analyze_wildcard=True)
s = s.filter('range', ** {'@timestamp': {'gte': start, 'lt': end}})

response = s.scan()

for hit in response:
    if query in json.loads(hit.result)['result']:
        print json.loads(json.loads(hit.result)['result'])['url']

