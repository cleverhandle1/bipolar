# bipolar
## preqreq
proxychains in worker path
redis installed and running somewhere
elasticsearch installed
## installation
git clone https://github.com/cleverhandle1/bipolar.git
cd bipolar
pip install -r requirements
 export SHODAN_API="<apikey>"
 export REDIS_PASS="<password>"
 export REDIS_HOST=localhost
## start worker
python bipolar/bipolar.py
## queue up jobs
python bipolar/scan_net.py 1.1.1.0/24
