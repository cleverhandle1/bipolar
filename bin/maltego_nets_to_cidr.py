import ipaddr

with open('nets.txt') as f:
    data = f.readlines()
nets = []
for d in data:
    nets.append(d.strip().split('-'))
for net in nets:
    start = ipaddr.IPv4Address(net[0])
    end = ipaddr.IPv4Address(net[1])
    print(ipaddr.summarize_address_range(start, end)[0])

