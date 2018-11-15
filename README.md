# bipolar
## purpose
the purpose of this project is to create an infinitely scaleable job worker infrastructure with a focus on offensive security tasks, such as port scanning and grabbing pages. tasks are extremely easy to modify or create from scratch. most connections are made via tor socks proxy running on localhost on the worker.

current list of pre-coded tasks:

* bipolar.http_get (pulls a page and returns the contents)
* bipolar.net_explode (takes a cidr address and returns an ip list)
* bipolar.proxy_check_socks (checks a host and port for socks proxies)
* bipolar.scan_hydra (starts hydra scan against a host)
* bipolar.scan_nmap (starts an nmap scan against a host)
* bipolar.sd_get_honeyscore (gets the honeyscore of a host from shodan)
* bipolar.sd_get_host (gets host information from shodan)
* bipolar.sd_get_ip_details (gets ip information from shodan)
* bipolar.sd_get_ips (general function)
* bipolar.sd_get_search (returns a list of ips based on a shodan query)
* bipolar.sqli_check (runs a sqlmap against a url)

job workers connect to redis (required), host creating jobs runs elasticsearch for job output (optional but highly recommended), jobs are distributed equally across multiple workers, tasks are executed and, if enabled, tor is used.
## preqreq
* proxychains in worker path
* tor proxy running on localhost:9050
* redis installed and running somewhere, redis password required, you're welcome
* elasticsearch installed locally to the job queuer (for output of some jobs)
* shodan api key, it's used by the worker.  it's free, go get one
## installation
```git clone https://github.com/cleverhandle1/bipolar.git
cd bipolar
pip install -r requirements
 export SHODAN_API="<apikey>"
 export REDIS_PASS="<password>"
 export REDIS_HOST=localhost
```

## start worker
```python bipolar/bipolar.py```

## queue up jobs
```python bipolar/scan_net.py 1.1.1.0/24```

## bin
jobs in the bin directory need to be moved into the bipolar directory that contains bipolar.py if you want to use them.
