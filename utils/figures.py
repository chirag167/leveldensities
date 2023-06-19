import colorlover as cl
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
from sklearn import metrics
from pickle import dump, load
import pandas as pd
from functools import partial
from plotly.tools import mpl_to_plotly


def lineplot(N, Z):
    
    layout = go.Layout(title=f'N={N}, Z={Z}')
    traces = [go.Scatter(x=[], y=[], mode='lines')]

    return go.Figure(data=traces, layout=layout)

