#!/usr/bin/env python
import json
import sys
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import QueryString
from elasticsearch import Elasticsearch

query = sys.argv[1]

es = Elasticsearch()

s = Search(using=es, index="celery") 
s = s.query("query_string", query=query, analyze_wildcard=True)

response = s.scan()

for hit in response:
    if query in json.loads(json.loads(hit.result)['result'])['content']:
        print json.loads(json.loads(hit.result)['result'])['url']

