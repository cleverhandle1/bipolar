import shodan
import os
import json

api_key = os.environ['SHODAN_API']

def get_sd_host(a):
    print('executing shodan query on: {}'.format(a))
    try:
        sd = shodan.Shodan(api_key, proxies={'http':'socks5://localhost:9050',
                                             'https':'socks5://localhost:9050'})
        result = sd.host(a)
        print('query complete on: {}'.format(a))
        return(result)
    except Exception as e:
        print('query failed for:{} :{}'.format(a, e))
        pass

def get_sd_search(a):
    print('executing shodan query on: {}'.format(a))
    try:
        sd = shodan.Shodan(api_key, proxies={'http':'socks5://localhost:9050',
                                             'https':'socks5://localhost:9050'})
        result = sd.search(a)
        print('query complete on: {}'.format(a))
        return(result)
    except Exception as e:
        print('query failed for:{} :{}'.format(a, e))
        pass

def get_sd_honeyscore(a):
    print('executing shodan honeyscore query on: {}'.format(a))
    try:
        sd = shodan.Shodan(api_key, proxies={'http':'socks5://localhost:9050',
                                             'https':'socks5://localhost:9050'})
        result = sd.labs.honeyscore(a)
        print('honeyscore query complete on: {}'.format(a))
        return(json.dumps({'ip':a, 'result':result}))
    except Exception as e:
        print('query failed for:{} :{}'.format(a, e))
        pass

def get_sd_ips(a):
    data = json.loads(a)
    ips = []
    for match in data['matches']:
        ips.append(match['ip_str']) 
    return ips

