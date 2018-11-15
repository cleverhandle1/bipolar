#!/usr/bin/env python
import sys
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import QueryString
from elasticsearch import Elasticsearch

query = sys.argv[1]

es = Elasticsearch()

s = Search(using=es, index="fnhttp") 
s = s.query("query_string", query=query, analyze_wildcard=True)

response = s.scan()

for hit in response:
    print(hit.url)
