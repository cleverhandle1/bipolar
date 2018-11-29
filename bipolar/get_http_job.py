from elasticsearch import Elasticsearch
import json
import sys

es = Elasticsearch()

try:
    res = es.get(index="celery", doc_type='backend', id='celery-task-meta-' + sys.argv[1])
    print(json.loads(json.loads(res['_source']['result'])['result'])['content'])
except Exception as e:
    print(e)

