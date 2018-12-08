#!/usr/bin/env python
import sys
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

index = sys.argv[1]
query_port = int(sys.argv[2])
start = sys.argv[3]
end = sys.argv[4]

es = Elasticsearch(hosts=['192.168.0.69'])

s = Search(using=es, index=index)
s = s.query("query_string", query='open_port:{}'.format(query_port), analyze_wildcard=True)
s = s.filter('range', ** {'@timestamp': {'gte': start, 'lt': end}})

response = s.scan()

for res in response:
    print(res.ip)
    
