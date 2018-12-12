#!/usr/bin/env python
from __future__ import absolute_import, unicode_literals
from celery import Celery, current_app
from celery.bin import worker
from time import sleep
from modules.sd import *
from modules.scan import *
import json
import os
import sys

redis_pass = os.environ['REDIS_PASS']
redis_host = os.environ['REDIS_HOST']

#app = Celery('bipolar',
#              broker='redis://redis:{}@{}'.format(redis_pass, redis_host),
#              backend='redis://redis:{}@{}'.format(redis_pass, redis_host),
#              fixups=[]
#            )

app = Celery('bipolar',
        broker='redis://redis:{}@{}'.format(redis_pass, redis_host),
        backend='elasticsearch://192.168.0.69:9200',
        fixups=[]
            )
app.conf.update({
    'task_routes': {
        'heartbleed_scan': {'queue': 'scan'}
    },
    'routes': {
        'heartbleed_scan': {'queue': 'scan'}
    },
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']})

@app.task
def sd_get_host(a):
    result = get_sd_host(a)
    result = json.dumps(result)
    return result 

@app.task
def sd_get_search(a):
    result = get_sd_search(a)
    result = json.dumps(result)
    return result 

@app.task
def sd_get_honeyscore(a):
    result = get_sd_honeyscore(a)
    return result 

@app.task
def sd_get_ip_details(a):
    result = get_sd_ip_details(a)
    result = json.dumps(result)
    return result

@app.task
def sd_get_ips(a):
    result = get_sd_ips(a)
    return result

@app.task
def net_explode(ip_net):
    result = explode_net(ip_net) 
    return result

@app.task(queue='scan')
def scan_nmap(ip):
    result = nmap_scan(ip)
    return result 

@app.task(queue='scan')
def scan_heartbleed(ip):
    result = heartbleed_scan(ip)
    return result 

#todo
@app.task
def scan_hydra(ip):
    result = hydra_scan(ip)
    return result 

@app.task
def proxy_check_socks(ip, port):
    result = check_proxy_socks(ip, port)
    return result

@app.task
def http_get(url):
    result = get_http(url)
    return result

@app.task
def sqli_check(url):
    result = check_sqli(url)
    return result

@app.task(queue='scan')
def heartbleed_get(ip):
    result = get_heartbleed(ip)
    return result

@app.task
def cert_get(ip):
    result = get_cert(ip)
    return result

@app.task
def scan_dns_recursion(ip):
    result = dns_recursion_scan(ip)
    return result

if __name__ == '__main__':
    app = current_app._get_current_object()

    worker = worker.worker(app=app)

    options = {
        'loglevel': 'INFO',
        'traceback': True,
        'concurrency': 50

    }

    worker.run(**options)
