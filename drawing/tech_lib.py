from datetime import datetime
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subploys import make_subplots


## reference https://chart-studio.plotly.com/~jackp/17421/plotly-candlestick-chart-in-python/#/

INCREASING_COLOR = '#17BECF'
DECREASING_COLOR = '#7F7F7F'

LOCATIONS = {
    "above": -1,
    "main": 0,
    "below": 1,
}

GRAPH_TYPES = {
    "ohlc": go.ohlc,
    "candlestick": go.candlestick,
    "bar": go.Bar,
    "scatter": go.Scatter,
    "macd": draw_macd,
}

def draw_macd():
    pass

class GraphType:
    def __init__(self, name, location=None, type=None, param=None):
        self.name = name
        # location should be "above", "main", "below"
        self.location = location
        self.type = type if type is not None else GRAPH_TYPES[self.name]
        self.param = param


def init_subplots(gts):
    """ init a plot with subplots """
    # determine how many rows needed
    gts = sorted(gts, key=lambda g: LOCATIONS[g.locatioin])

    locations = [g.location for g in gts]
    assert "main" in locations
    rows = locations.count("above") + locations.count("below") + 1
    fig = make_subplots(rows=rows, cols=1)

    for i in range(len(gts)):
        # draw each row



def init_candlestick_chart(data):
    chart = [
        dict (
            type = 'candlestick',
            open = data.open,
            high = data.high,
            low = data.low,
            close = data.close,
            x = data.timestamp,
            yaxis = 'y2',
            name = 'CS',
            increasing = dict( line = dict( color = INCREASING_COLOR ) ),
            decreasing = dict( line = dict( color = DECREASING_COLOR ) ),
        ),
    ]
    layout = dict (
        plot_bgcolor = 'rgb(250, 250, 250)',
        xaxis = dict(rangeselector = dict( visible = True )),
        yaxis = dict(domain = [0, 0.2], showticklabels = False),
        yaxis2 = dict(domain = [0.2, 0.8]),
        legend = dict(orientation = 'h', y=0.9, x=0.3, yanchor='bottom'),
        margin = dict(t=40, b=40, r=40, l=40),
    )

    fig = dict(data=chart, layout=layout)
    