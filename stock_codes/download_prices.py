import argparse
import os
import json
import urllib3

URL_PATTERN = 'https://query1.finance.yahoo.com/v8/finance/chart/%s?region=US&lang=en-US&includePrePost=false&interval=%s&range=%s&corsDomain=finance.yahoo.com&.tsrc=finance'


def stock_download(symbol, interval, timerange):
    url = URL_PATTERN % (symbol.upper(), interval, timerange)

    http = urllib3.PoolManager()
    resp = http.request("GET", url)

    if resp.status > 299:
        raise ValueError("status code is not 200-299")
    c = resp.data.decode("utf-8")
    js = json.loads(c)
    
    quotes = js["chart"]["result"][0]["indicators"]["quote"][0]
    quotes["timestamp"] = js["chart"]["result"][0]["timestamp"]
    return quotes


def stocks_download_main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbol", 
                        default="aapl",
                        help="symbol")
    parser.add_argument("--output",
                        default=None,
                        help="directory to output csv files")
    parser.add_argument("--date",
                        default=None,
                        help="specify expiration date; if not set, download all")
    parser.add_argument("--interval",
                        default="1d",
                        help="specify interval, e.g., 1m, 5m, 1d, ...")
    parser.add_argument("--time-range",
                        default="1y",
                        help="specify time range, e.g., 1d, 1y, ...")
    opt = parser.parse_args()

    return stock_download(opt.symbol, opt.interval, opt.timerange)
