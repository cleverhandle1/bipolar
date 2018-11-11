import bipolar
from celery import group
from time import sleep
from elasticsearch import helpers, Elasticsearch
import sys
import json

query = sys.argv[1]
#'Server: SQ-WEBCAM'
query_results = bipolar.sd_get_search.delay(query).get()
ips = bipolar.sd_get_ips(query_results)
my_group = group([bipolar.sd_get_host.s(ip) for ip in ips])
group_results = my_group.apply_async()
while not group_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
group_results = group_results.get()

ip_data = {}
for results in group_results:
    results = json.loads(results)
    if results is not None:
        ip = results['ip_str']
        ip_data[ip] = results
    else:
        pass

my_group = group([bipolar.sd_get_honeyscore.s(ip) for ip in ips])
group_results = my_group.apply_async()
while not group_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
group_results = group_results.get()

for results in group_results:
    if results is not None:
        results = json.loads(results)
        ip = results['ip']
        score = results['result']
    else:
        pass 
    if ip in ip_data.keys():
        ip_data[ip]['honeypot_score'] = score
        ip_data[ip]['query'] = query

output = []
for ip in ip_data.keys():
    output.append(json.dumps({'ip': ip, 'data':ip_data[ip]}))

es = Elasticsearch()
helpers.bulk(es, output, index='fnsd', doc_type="doc")
