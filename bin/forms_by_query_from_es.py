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

s = Search(using=es, index="fnhttp")
qs = QueryString(query="form action")
s = s.query(qs)

response = s.scan()

final_urls = []
for hit in response:
    url = hit.url
    soup = BeautifulSoup(hit.content, 'html.parser')
    inputs = soup.find_all('input')
    field_names = []
    for i in inputs:
        if i.has_key('name'):
            field_names.append(i['name'])
    if field_names == []:
        pass
    else:
        params = '?' + '&'.join([x + "=asdf" for x in field_names])
        final_urls.append(url + params)
print(final_urls)


my_group = group([bipolar.sqli_check.s(url) for url in final_urls])
group_results = my_group.apply_async()
while not group_results.ready():
    print('waiting for jobs to complete')
    sleep(10)
    group_results = group_results.get()
