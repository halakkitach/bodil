#!/usr/bin/python3

# Vidio API Python
# Created by:  @halakkita

import argparse
import requests
import json
import re
import os
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-c", "--channel-code", required=True, help="channel code")
parser.add_argument("-n", "--channel-name", required=True, help="channel name")
parser.add_argument("output", nargs="?", help="output file")
args = parser.parse_args()

vidio_url = 'vidio.com'
windows = False
if 'win' in sys.platform:
    windows = True

def nosignal():
    url = 'http://halakkitach.github.io/ONLINE/erorya'
    m3u8_get = requests.get(f"{url}/index.m3u8").text
    for ts in ['260.m3u8', '360.m3u8', '480.m3u8', '720.m3u8', '1080.m3u8']:
        m3u8_get = m3u8_get.replace(ts, f"{url}/{ts}")
    return m3u8_get

def grab(code, name):
    headers = {}

    payload = {}
    payload['Authority'] = f"www.{vidio_url}"
    payload['Content-Length'] = '0'
    payload['Origin'] = f"https://www.{vidio_url}"
    payload['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
    payload['Dnt'] = '1'
    payload['Accept'] = '*/*'
    payload['Sec-Fetch-Site'] = 'same-origin'
    payload['Sec-Fetch-Mode'] = 'cors'
    payload['Referer'] = f"https://www.{vidio_url}/live/{code}-{name}";
    payload['Accept-Encoding'] = 'gzip, deflate, br';
    payload['Accept-Language'] = 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7';

    try:
        get = s.post(f"https://www.{vidio_url}/live/{code}/tokens", data=json.dumps(payload), headers=headers).json()
        if 'token' not in get:
            return nosignal()
        else:
            headers['Authority'] = f"app-etslive-2.{vidio_url}"
            headers['Origin'] = f"https://www.{vidio_url}"
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            headers['Dnt'] = '1'
            headers['Accept'] = '*/*'
            headers['Sec-Fetch-Site'] = 'same-site'
            headers['Sec-Fetch-Mode'] = 'cors'
            headers['Referer'] = f"https://www.{vidio_url}"
            headers['Accept-Encoding'] = 'gzip,deflate,br'
            headers['Accept-Language'] = 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'

            return s.get(f"https://app-etslive-2.{vidio_url}/live/{code}/master.m3u8?{get['token']}", headers=headers).text
    except:
        return nosignal()

s = requests.Session()
result = grab(args.channel_code, args.channel_name)
if args.output:
    open(args.output, "w").write(result)
else:
    print(result)
