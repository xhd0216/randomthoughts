import pandas as pd 
import cufflinks as cf


from randomthoughts.stock_codes.download_prices import stock_download


def get_stock_df(symbol, interval="1d", timerange="1y"):
    """ wrapper to stock_download """
    data = stock_download(symbol, interval, timerange)
    df = pd.core.frame.DataFrame.from_dict(data)
    df.set_index("date", inplace=True)

    return df


def get_image(symbol, interval, timerange):
    """ returns a html <div> of image """
    df = get_stock_df(symbol, interval, timerange)
    qf = cf.QuantFig(df)
    qf.add_bollinger_bands()
    qf.add_sma(5)
    qf.add_sma(10)
    qf.add_sma(20)
    qf.add_volume()
    qf.add_rsi()
    qf.add_macd()
 
    return qf.figure().to_html(full_html=True, include_plotlyjs=True)
