import time
import pandas as pd
import random as rand
import base64
from datetime import datetime, date

import dash
from dash import dcc
from dash import html
import numpy as np
from dash.dependencies import Input, Output, State
import json
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

import utils.dash_reusable_components as drc
import utils.figures as figs
from utils.views import *


app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.config.suppress_callback_exceptions=True
app.title = "Level Densities"
server = app.server

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),
    html.Div(className="banner", children=[
        html.Div(className="container scalable", children=[
            html.H2(id="banner-title", children=[
                html.A(id="banner-logo", href="https://bmex.dev", children=[
                    html.Img(src=app.get_asset_url("BMEX-logo-3.png"))
                ],),
            ],),
        ],),
    ],),
    html.Div(id='page-content'),
    dcc.Store(id="download-memory"),
    dcc.Download(id="data-download"),
])

@app.callback(
    Output('page-content','children'),
    [Input('url','pathname')]
    )
def display_page(pathname):
    # if(pathname == "/leveldensities"):
    #     out = view()
    # else:
    #     out = html.Div(
    #         id="body",
    #         className="container scalable",
    #         children=[html.P("How did you get here? Click the banner to make it back to safety!")])
    out = view()
    return out

@app.callback(
    Output("div-graphs", "children"),
    # Output("download-memory", "data"),
    [
        Input("neutron-input", "value"),
        Input("proton-input", "value"),
    ]
)
def main_output(N, Z):
    if N == None or Z == None:
        return html.P("Please enter an N and Z")
    return \
        [dcc.Graph(id="graph", figure=figs.lineplot(N,Z))]

@app.callback(
    Output("samples-download", "data"),
    Input("download-button", "n_clicks"),
    State("download-memory", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, data):
    if n_clicks == None or data == None:
        raise PreventUpdate
    filename = "LDdata-"+str(date.today().strftime("%b%d-%Y"))+"_"+str(datetime.now().strftime("%H:%M:%S"))+".csv"
    data = pd.DataFrame(json.loads(data))
    def write_csv(bytes_io):
        # write csv to bytes_io
        data.to_csv(bytes_io, index=False, encoding='utf-8-sig')
    return dcc.send_bytes(write_csv, filename) 

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=True, use_reloader=True)
   