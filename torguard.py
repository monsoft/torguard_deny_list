#!/usr/bin/env python3

import socket
import pandas as pd
import os
import requests
import sys

ipset_file = 'torguard_ipset.txt'
ipset_file_cache = 'torguard_ipset.cache'
ipset_set = 'torguard'
url = 'https://torguard.net/network/index.php'
http_headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'}


# Remove file if exist
if os.path.exists(ipset_file):
    os.remove(ipset_file)

print('TorGuars nodes IP builder by Irek \'Monsoft\' Pelech')
print('')

try:
    page = requests.get(url, headers=http_headers)
    page.raise_for_status()
except requests.exceptions.HTTPError as e:
    sys.exit("Error: " + str(e))
    
hn_tables = pd.read_html(page.text, header=None, index_col=None)
print('Generating %s ipset list' % ipset_file_cache )

for i in range(len(hn_tables)):
    with open(ipset_file_cache, 'a') as f:
        hn_table = hn_tables[i]['Hostnames'].to_numpy()
        for host_name in hn_table:
            #print(host_name, socket.gethostbyname_ex(host_name)[2])
            for ip in socket.gethostbyname_ex(host_name)[2]:
                print('add %s %s' % (ipset_set,ip), file=f)
                print('■', end='', flush=True)

os.system('sort -u %s >> %s' % (ipset_file_cache, ipset_file))
os.remove(ipset_file_cache)
print('')
print('IPs have been written to %s file. Please import it to your ipset list.' % ipset_file)
