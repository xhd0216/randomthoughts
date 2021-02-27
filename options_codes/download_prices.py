import argparse
import datetime
import urllib3
import json
from pathlib import Path

YAHOO_URL = "https://finance.yahoo.com/quote/%s/options/"
PATTERN = "root.App.main = "


def download_origin(symb, with_date=None):
    """ download the original data from yahoo """
    http = urllib3.PoolManager()
    if with_date is not None:
        url = (YAHOO_URL[:-1] + "?date=%s") % (symb, with_date)
    else:
        url = YAHOO_URL % symb
    resp = http.request("GET", url)
    # check if response is good
    if resp.status > 299:
        raise ValueError("invalid response status", resp.status)
    return resp


def extract_data_wrapper(symbol):
    """ wrapper """
    resp = download_origin(symbol)
    return extract_data(resp)

def extract_data(resp):
    """
        extract data from http resp 
        options data resides in the html in a function.
    """
    data = resp.data.decode()
    idx = data.find(PATTERN)
    start = idx + len(PATTERN)
    end = start
    cnt = 0
    try:
        while True:
            if data[end] == "{":
                cnt += 1
            elif data[end] == "}":
                cnt -= 1
            if cnt == 0:
                break
            end += 1
    except Exception:
        raise ValueError("error parsing html data")

    a = json.loads(data[start:end+1])
    x = a["context"]["dispatcher"]["stores"]["OptionContractsStore"]
    meta = x["meta"]
    contracts = x["contracts"]
    return contracts, meta


def get_long_int_time(t):
    """ given datetime object, return the long int format of it """
    return int(t.timestamp())


DATE_TIME_FORMAT = "%Y%m%d"

def create_options_file_name(symbol, exp_date="all", cur_time=None):
    """ given a path, return the file name """
    if cur_time is None:
        cur_time = get_long_int_time(datetime.datetime.now())
    if type(exp_date) == int:
        exp_date = datetime.datetime.fromtimestamp(exp_date)
    if type(exp_date) == datetime.datetime:
        exp_date = exp_date.strftime(DATE_TIME_FORMAT)
    return "%s_%d_%s.csv" % (symbol, cur_time, exp_date)

def options_download_main():
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
    opt = parser.parse_args()

    if opt.output is not None:
        output = Path(opt.output)
    else:
        output = Path("./options_data_output")
    if not output.exists():
        output.mkdir()
    if not output.is_dir():
        raise ValueError("directory " + output.absolute() + " already exists and is not a directory")

    
    command_time = get_long_int_time(datetime.datetime.now())

    resp = download_origin(opt.symbol)
    contracts, meta = extract_data(resp)
    for d in meta["expirationDates"]:
        resp = download_origin(opt.symbol, with_date=d)
        contracts, _ = extract_data(resp)
        calls = contracts["calls"]
        puts = contracts["puts"]

        with open(output / create_options_file_name(opt.symbol, d, command_time), "w") as f:
            for i in range(len(calls)):
                if i == 0:
                    continue
                last = calls[i-1]
                now = calls[i]
                spread = now["strike"]["raw"] - last["strike"]["raw"]
                price = last["bid"]["raw"] - now["ask"]["raw"]
                f.write(','.join([now["expiration"]["fmt"], last["strike"]["fmt"], "%.2f" % spread, "%.2f" % price]) + "\n")
                print("date:", now["expiration"]["fmt"], "strike:", last["strike"]["fmt"], "spread: %.2f" % spread, "price: %.2f" % price)
            print("===================", d)

if __name__ == "__main__":
    options_download_main()