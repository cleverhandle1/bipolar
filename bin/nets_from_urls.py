#!/usr/bin/env python
import ipaddr
import urlparse
import dns.resolver
import whois
import json
from ipwhois import IPWhois
from time import sleep
import sys

input_file = sys.argv[1]

with open(input_file) as f:
    urls = f.readlines()

urls = [x.strip() for x in urls]

output = {}
for url in urls:
    parsed = urlparse.urlparse(url)
    hostname = parsed.netloc

    a = dns.resolver.query(hostname, 'A')
    a_rr = [rdata.address for rdata in a]
    
    try:
        whois_info = whois.whois(url)
    except Exception as e:
        print(e)
        whois_info = {}
        pass
    ipwhois_info = []
    try:
        ipwhois_info = [IPWhois(ip).lookup_whois() for ip in a_rr]
    except Exception as e:
        print(e)
        ipwhois_info = []
        pass

    if whois_info != {}:
        tmp_creation_date = whois_info['creation_date']
        if type(tmp_creation_date) == list:
            whois_info['creation_date'] = []
            for date in tmp_creation_date:
                whois_info['creation_date'].append(date.strftime('%Y-%m-%d'))
        else:
            whois_info['creation_date'] = whois_info['creation_date'].strftime('%Y-%m-%d')
        
        tmp_expiration_date = whois_info['expiration_date']
        if type(tmp_expiration_date) == list:
            whois_info['expiration_date'] = []
            for date in tmp_expiration_date:
                whois_info['expiration_date'].append(date.strftime('%Y-%m-%d'))
        else:
            whois_info['expiration_date'] = whois_info['expiration_date'].strftime('%Y-%m-%d')

        tmp_updated_date = whois_info['updated_date']
        if type(tmp_updated_date) == list:
            whois_info['updated_date'] = []
            for date in tmp_updated_date:
                whois_info['updated_date'].append(date.strftime('%Y-%m-%d'))
        else:
            whois_info['updated_date'] = whois_info['updated_date'].strftime('%Y-%m-%d')


    output[hostname] = {}
    output[hostname]['hostname'] = hostname
    output[hostname]['whois'] = whois_info
    output[hostname]['ip_whois'] = ipwhois_info
    output[hostname]['a_rr'] = a_rr

    sleep(5)
with open('data/output/isis/net_data_from_urls.json', 'w') as f:
    f.write(json.dumps(output))

print(json.dumps(output, indent=4))

for h in output.keys():
    print(h)
    for ip_whois in output[h]['ip_whois']:
        if ip_whois is not None:
            print(ip_whois['query'])
            print(ip_whois['asn_description'])
            print(ip_whois['asn_cidr'])
            print('')
    print('')

