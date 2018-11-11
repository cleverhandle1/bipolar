#!/usr/bin/env python
import sys
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

port = sys.argv[1]

es = Elasticsearch()

s = Search(using=es, index="fnscan") \
    .filter("term", open_ports=port )\

response = s.scan()

for hit in response:
    print(hit.ip)
