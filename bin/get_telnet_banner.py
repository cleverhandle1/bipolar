import getpass
import sys
import telnetlib

HOST = sys.argv[1]
user = 'admin'
password = 'admin'

tn = telnetlib.Telnet(HOST)
print tn.read_all()
tn.close()
