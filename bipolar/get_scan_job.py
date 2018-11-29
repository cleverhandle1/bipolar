from elasticsearch import Elasticsearch
import json
import sys

es = Elasticsearch()

try:
    res = es.get(index="celery", doc_type='backend', id='celery-task-meta-' + sys.argv[1])
    json_res = json.loads(res['_source']['result'])['result']
    for ip in json_res['scan'].keys():
        open_ports = []
        if 'tcp' in json_res['scan'][ip].keys():
            for port in json_res['scan'][ip]['tcp'].keys():
                state = json_res['scan'][ip]['tcp'][port]['state']
                if state == 'open':
                    open_ports.append(int(port))
        print(json.dumps({'ip': ip, 'open_ports':open_ports}))

except Exception as e:
    print(e)


