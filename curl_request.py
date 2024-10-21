import os
import requests
import subprocess
from http.client import HTTPConnection
import logging


logging.basicConfig(level=logging.DEBUG)
HTTPConnection.debuglevel = 1


root_ca = "/etc/ssl/certs/rootCA.pem"
url_base = "https://src-data-repo.co.uk/torkeep/observations/EMERLIN/"
xml_file = 'TS8004_C_001_20190801.xml'
data_dir = '/home/h14471mj/e-merlin/em_github/emerlin2caom/emerlin2caom2/data/'
ska_token = ''


def curl_request(xml_file, data_dir, root_ca, ska_token, url_base):
    url_end = xml_file.split('.')[0]
    url = url_base + url_end
    with open(data_dir + xml_file, 'r') as f:
        content = f.read()
    headers = {'Content-Type': 'text/xml', 'authorization': 'bearer {}'.format(ska_token)}
    r = requests.put(url, data=content, headers=headers, verify=root_ca)


curl_request(xml_file, data_dir, root_ca, ska_token, url_base)
