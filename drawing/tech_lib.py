import pandas as pd 
import cufflinks as cf


from stock_codes.download_prices import stock_download


def get_stock_df(symbol, interval="1d", timerange="1y"):
    """ wrapper to stock_download """
    data = stock_download(symbol, interval, timerange)
    df = pd.core.frame.DataFrame.from_dict(data)
    df.set_index("date", inplace=True)

    return df


def get_image():
    """ returns a html <div> of image """
    symbol = "tsla"
    interval = "1d"
    timerange = "1y"

    df = get_stock_df(symbol, interval, timerange)
    qf = cf.QuantFig(df)
    qf.add_bollinger_bands()
    qf.add_volume()
    return qf.figure().to_html(full_html=True, include_plotlyjs=True)
