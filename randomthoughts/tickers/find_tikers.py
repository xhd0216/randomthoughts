import queue
import re
import urllib3
import urllib.parse

all_tickers = set("spy")
url_p = "https://finance.yahoo.com/quote/%s?p=%s"
sp_list_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

def get_sp_500():
    http = urllib3.PoolManager()
    resp = http.request("GET", sp_list_url)
    if resp.status != 200:
        return None

    page = resp.data.decode()
    ind = [m.end() for m in re.finditer("https://www.nyse.com/quote/XNYS:", page)]
    temp_list = [page[m:m+10] for m in ind]
    res = [t[:t.find("\"")] for t in temp_list]
    return res

def get_one(symb):
    symb = symb.upper()
    url = url_p % (symb, symb)
    http = urllib3.PoolManager()
    resp = http.request("GET", url)
    if resp.status != 200:
        print("Failed to fetch", url, resp.status)
    page = resp.data.decode()
    ind = [m.end() for m in re.finditer("/quote/", page)]
    temp_list = [page[m:m+10] for m in ind]
    res = [t[:t.find("?")] for t in temp_list if "?" in t]
    res = [r for r in res if "/" not in r]
    return res

def main():
    q = queue.Queue()
    sp500 = get_sp_500()
    for r in sp500:
        q.put(r)
    checked = set()
    while not q.empty():
        s = q.get()
        s = s.upper()
        s = urllib.parse.unquote(s)
        if "." in s or "=" in s:
            continue
        if s in checked:
            continue
        checked.add(s)
        res = get_one(s)
        for r in res:
            q.put(r)
        if len(checked) > 1000:
            break
    for c in sorted(checked):
        print(c)
    print(len(checked))

if __name__=="__main__":
    main()
    
