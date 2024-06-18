#!/usr/bin/python3

# Vidio API Python
# Created by: @halakkita

import argparse
import requests
import json
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

def m3u8_get():
    url = 'https://www.vidio.com/live'
    m3u8_get = requests.get(f"{url}/index.m3u8").text
    for ts in ['260.m3u8', '360.m3u8', '480.m3u8', '720.m3u8', '1080.m3u8']:
        m3u8_get = m3u8_get.replace(ts, f"{url}/{ts}")
    return m3u8_get

def grab(code, name):
    headers = {
        'Authority': f"www.{vidio_url}",
        'Content-Length': '0',
        'Origin': f"https://www.{vidio_url}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
        'Dnt': '1',
        'Accept': '*/*',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Referer': f"https://www.{vidio_url}/live/{code}-{name}",
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
    }

    try:
        get = s.post(f"https://www.{vidio_url}/live/{code}/tokens", headers=headers).json()
        if 'token' not in get:
            return m3u8_get()
        else:
            headers['Authority'] = f"app-etslive-2.{vidio_url}"
            headers['Origin'] = f"https://www.{vidio_url}"
            headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
            headers['Sec-Fetch-Site'] = 'same-site'
            headers['Sec-Fetch-Mode'] = 'cors'
            headers['Referer'] = f"https://www.{vidio_url}"

            return s.get(f"https://app-etslive-2.{vidio_url}/live/{code}/master.m3u8?{get['token']}", headers=headers).text
    except Exception as e:
        print(f"An error occurred: {e}")
        return m3u8_get()

s = requests.Session()
result = grab(args.channel_code, args.channel_name)
if args.output:
    with open(args.output, "w") as f:
        f.write(result)
else:
    print(result)
