#!/usr/bin/env python
import sys
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch

query_port = int(sys.argv[1])

es = Elasticsearch()

s = Search(using=es, index="celery")
s = s.query("query_string", query='scanstats', analyze_wildcard=True)

response = s.scan()

for res in response:
    json_res = json.loads(res.result)['result']
    for ip in json_res['scan'].keys():
        open_ports = []
        if 'tcp' in json_res['scan'][ip].keys():
            for port in json_res['scan'][ip]['tcp'].keys():
                state = json_res['scan'][ip]['tcp'][port]['state']
                if state == 'open':
                    open_ports.append(int(port))
        if query_port in open_ports:
            print(ip)

