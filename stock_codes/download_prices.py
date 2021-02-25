import os
import json
import urllib3


symbol = input("please input the symbol:")
if not symbol:
    symbol = "TSLA"
interval = input("please specify interval, e.g., 1m, 5m, 1d, ...")
if not interval:
    interval = "1m"
timerange = input("please specify time range, e.g., 1d, 1y, ...")
if not timerange:
    timerange = "1d"
url_pattern = 'https://query1.finance.yahoo.com/v8/finance/chart/%s?region=US&lang=en-US&includePrePost=false&interval=%s&range=%s&corsDomain=finance.yahoo.com&.tsrc=finance'
url = url_pattern % (symbol.upper(), interval, timerange)

http = urllib3.PoolManager()

resp = http.request("GET", url)

if resp.status > 299:
    raise ValueError("status code is not 200-299")

c = resp.data.decode("utf-8")

js = json.loads(c)

quotes = js["chart"]["result"][0]["indicators"]["quote"][0]

closes = quotes['close']
highs = quotes['high']
lows = quotes['low']
opens = quotes['open']
volumes = quotes['volume']



timestamps = js["chart"]["result"][0]["timestamp"]


print(opens)
