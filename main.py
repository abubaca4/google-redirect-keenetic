import urllib.request
import json
from ipaddress import IPv4Network

ipv4_taget_interface = 'Wireguard0'
ipv6_taget_interface = ipv4_taget_interface

result_file_name = "result.txt"

with urllib.request.urlopen('https://www.gstatic.com/ipranges/goog.json') as f:
    data = json.loads(f.read().decode('utf-8'))
    ipv4_list = []
    ipv6_list = []
    for net in data["prefixes"]:
        if net.get('ipv4Prefix') is not None:
            ipv4_list.append(net["ipv4Prefix"])
        else:
            ipv6_list.append(net["ipv6Prefix"])
    with open(result_file_name, "w", encoding='utf-8') as output:
        ipv4_count = 0
        for net in ipv4_list:
            network = IPv4Network(net)
            output.write("ip route " + str(network.network_address) + " " + str(network.netmask) + " " + ipv4_taget_interface + " auto " + "!google " + str(ipv4_count) + "\n")
            ipv4_count += 1
        ipv6_count = 0
        for net in ipv6_list:
            output.write("ipv6 route " + net + " " + ipv6_taget_interface + " auto " + "!google6 " + str(ipv6_count) + "\n")
            ipv6_count += 1
        output.close()