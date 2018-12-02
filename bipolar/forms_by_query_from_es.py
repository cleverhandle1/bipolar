#!/usr/bin/env python
import sys
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import QueryString
from elasticsearch import helpers, Elasticsearch
from bs4 import BeautifulSoup
from celery import group
import bipolar
from time import sleep
import json

query = sys.argv[1]
es = Elasticsearch()

s = Search(using=es, index="celery")
s = s.query("query_string", query=query, analyze_wildcard=True)

response = s.scan()

final_urls = []
for hit in response:
    if query in json.loads(json.loads(hit.result)['result'])['content']:
    	url = json.loads(json.loads(hit.result)['result'])['url']
    	soup = BeautifulSoup(json.loads(json.loads(hit.result)['result'])['content'], 'html.parser')
        inputs = soup.find_all('input')
        field_names = []
        for i in inputs:
            if i.has_attr('name'):
                field_names.append(i['name'])
        if field_names == []:
            pass
        else:
            params = '?' + '&'.join([x + "=admin" for x in field_names])
            final_urls.append(url + params)
for url in final_urls:
    print(url)
    #
    #
    #my_group = group([bipolar.sqli_check.s(url) for url in final_urls])
    #group_results = my_group.apply_async()
    #while not group_results.ready():
    #    print('waiting for jobs to complete')
    #    sleep(10)
    #    group_results = group_results.get()
