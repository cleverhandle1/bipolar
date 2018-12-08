#!/usr/bin/env python
import sys
import json
from elasticsearch_dsl import Search
from elasticsearch import Elasticsearch, helpers

es = Elasticsearch(hosts=['192.168.0.69:9200'], timeout=999999)

index = sys.argv[1]
start = sys.argv[2]
end = sys.argv[3]

s = Search(using=es, index="celery")
s = s.query("query_string", query='scanstats AND open', analyze_wildcard=True)
s = s.filter('range', ** {'@timestamp': {'gte': start, 'lt': end}})

response = s.scan()

print('reading from es')
output = []
for res in response:
    doc_id = res.meta.id
    timestamp = res['@timestamp']
    json_res = json.loads(res.result)['result']
    for ip in json_res['scan'].keys():
        if 'tcp' in json_res['scan'][ip].keys():
            for port in json_res['scan'][ip]['tcp'].keys():
                state = json_res['scan'][ip]['tcp'][port]['state']
                if state == 'open':
                    output.append({'ip':ip, 'open_port':int(port), '@timestamp':timestamp})

print('sending to es')
helpers.bulk(es, output, index=index, doc_type="doc")

#while not group1_results.ready(): #    print('waiting for jobs to complete')
#    sleep(10)
#group1_results = group1_results.get()
#
#output = []
#for results in group1_results:
#    if results is not None:
#        output.append(json.loads(results))
#
#es = Elasticsearch(timeout=999999)
#helpers.bulk(es, output, index='fnhttp', doc_type="doc")
#
#print(output)

