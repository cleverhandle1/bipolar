import ipaddr
import nmap
from random import shuffle
import requests
import json
import subprocess
import ssl

def explode_net(ip_net):
    ips = [x.exploded for x in ipaddr.IPNetwork(ip_net).iterhosts()]
    shuffle(ips)
    if ips == []:
        ips = [ipaddr.IPNetwork(ip_net).ip.exploded]
    return ips
  
def nmap_scan(ip):
    print('executing nmap scan against: {}'.format(ip))
    nm = nmap.PortScanner()
    scan_results = nm.scan(hosts=ip, arguments='-sT --top-ports=20 -Pn -T polite')
    return scan_results 

def check_proxy_socks(ip, port):
    outputs = []
    print('trying: {}:{}'.format(ip,port))
    proxies = {'http':'socks5://{}:{}'.format(ip,port)}
    try:
        results = requests.get('http://ipinfo.io', proxies=proxies, timeout=10).text
        try:
            data = json.loads(results)
            output = {'ip': ip, 'port': str(port), 'is_proxy':True, 'proxies':proxies}
            outputs.append(output)
        except Exception as e:
            output = {'ip': ip, 'port': str(port), 'is_proxy':False, 'error':e}
            outputs.append(output)
    except Exception as e:
        print(e)

    proxies = {'https':'socks5://{}:{}'.format(ip,port)}
    try:
        results = requests.get('https://ipinfo.io', proxies=proxies, timeout=10).text
        try:
            data = json.loads(results)
            output = {'ip': ip, 'port': str(port), 'is_proxy':True, 'proxies':proxies}
            outputs.append(output)
        except Exception as e:
            output = {'ip': ip, 'port': str(port), 'is_proxy':False, 'error':e}
            outputs.append(output)
    except Exception as e:
        print(e)
    return outputs

def get_http(url):
    try:
        result = requests.get(url, proxies={'http':'socks5://localhost:9050', 'https':'socks5://localhost:9050'}, timeout=30)
        output = json.dumps({'status': result.status_code, 'content': result.content, 'url':url}, encoding='ISO-8859-1') 
        return output
    except Exception as e:
        print(e)
        pass

def check_sqli(url):
    try:
        result = subprocess.check_output(
            "proxychains4 -q ~/src/sqlmap/sqlmap.py --batch -a --random-agent -u '{}'".format(url),
            stderr=subprocess.STDOUT,
            shell=True)
        return result
    except Exception as e:
        print(e)
        return e

def get_cert(ip):
    import socks_new
    s = socks.socksocket()
    s.setproxy(socks.PROXY_TYPE_SOCKS5,"localhost", 9050)
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    s = ctx.wrap_socket(s, server_hostname=ip)
    s.connect((ip, 443))
    cert = s.getpeercert()
    return cert
