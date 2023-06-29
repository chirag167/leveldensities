import time
import os
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
    ''' Function to display the page'''
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
def main_output(Z, A):
    '''The main function'''
    nld_log_file = pd.read_excel('Arranged data.xlsx')
    nld_log_file.dropna(subset=['Datafile'],inplace = True)
    nld_log_file.drop('Datafile',inplace=True,axis=1)
    nld_log_file = nld_log_file.reset_index()
    nld_log_file['Validation'] = nld_log_file['Validation'].replace(np.nan,'yes')

    nld_folder = str(Z) + '_' + str(A)
    data_frames = []

    for filename in os.listdir(nld_folder):
        if filename.endswith('.csv'):
            file_path = os.path.join(nld_folder, filename)
            nld_file = pd.read_csv(file_path, comment='#', header=None)
            nld_file.drop(3, axis=1, inplace=True)
            nld_file.rename(columns={0: "E (MeV)", 1: r"$\rho$", 2: r"$\delta \rho$"}, inplace=True)
            data_frames.append(nld_file)

    if A is None or Z is None:
        return html.P("Please enter an A and Z")
            

    return data_frames,nld_log_file[(nld_log_file['Z'] == Z) & (nld_log_file['A'] == A)]

    
    #return \
        #[dcc.Graph(id="graph", figure=figs.lineplot(N,Z))]

@app.callback(
    Output("samples-download", "data"),
    Input("download-button", "n_clicks"),
    State("download-memory", "data"),
    prevent_initial_call=True,
)
def download(n_clicks, data):
    '''Function to download the data files'''
    if n_clicks is None or data is None:
        raise PreventUpdate
    filename = "LDdata-"+str(date.today().strftime("%b%d-%Y"))+ \
    "_"+str(datetime.now().strftime("%H:%M:%S"))+".csv"    
    data = pd.DataFrame(json.loads(data))
    def write_csv(bytes_io):
        # write csv to bytes_io
        data.to_csv(bytes_io, index=False, encoding='utf-8-sig')
    return dcc.send_bytes(write_csv, filename) 

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, dev_tools_hot_reload=True, use_reloader=True)
   