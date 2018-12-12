#!/usr/bin/env python
import json
import sys
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import QueryString
from elasticsearch import Elasticsearch

query = "ssl-heartbleed AND vulnerable"

es = Elasticsearch('192.168.0.69')

s = Search(using=es, index="celery") 
s = s.query("query_string", query=query, analyze_wildcard=True)

response = s.scan()

for hit in response:
    print json.loads(hit.result)['result']['scan'].keys()[0]

