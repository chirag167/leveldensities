import time
import os
import pandas as pd
import random as rand
import base64
from datetime import datetime, date

import dash
from dash import dash_table
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

#df = pd.read_csv('26_56/NLD_26_56_4.csv',comment='#',header=None)

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
    #dash_table.DataTable(df.to_dict('records'))
])

@app.callback(
    #Output("div-graphs", "children"),
    Output("download-memory", "data"),
    [
        Input("A", "value"),
        Input("Z", "value"),
    ]
)
def main_output(A, Z):
    '''The main function'''
    # The arranged data excel sheet is uploaded to GitHub
    nld_log_file = pd.read_csv('Arranged_data.csv',header=0,sep=',')
    # Drop the rows where the datafile doesn't exist
    nld_log_file.dropna(subset=['Datafile'],inplace = True)
    nld_log_file = nld_log_file.reset_index()
    # drop the datafile column because I will display the data on the website itself.
    nld_log_file.drop('Datafile',inplace=True,axis=1)
    nld_log_file['Validation'] = nld_log_file['Validation'].replace(np.nan,'yes')

    nld_folder = str(Z) + '_' + str(A) # data folder is formatted as Z_A
    #data_frames = []

    for filename in os.listdir(nld_folder):
        # only csv files have been checked and validated yes/no.
        if filename.endswith('.csv'):
            file_path = os.path.join(nld_folder, filename)
            # the first 2 or 3 lines in each csv file is just comments (to be ignored) starting with hashtag
            nld_file = pd.read_csv(file_path, comment='#', header=None)
            # the dataframe also includes an extra column. So I am dropping it.
            nld_file.drop(3, axis=1, inplace=True)
            # renaming columns
            nld_file.rename(columns={0: "E (MeV)", 1: "NLD", 2: "NLD uncertainity"}, inplace=True)
            #data_frames.append(nld_file)
    
    if A is None or Z is None:
        return html.P("Please enter an A and Z")
    # return values of the function: the data frames containing the data and the log file containing general information about that isotope.
    return dash_table.DataTable(nld_file.to_dict('records')) #,nld_log_file[(nld_log_file['Z'] == Z) & (nld_log_file['A'] == A)] , [dcc.Graph(id="graph", figure=figs.lineplot(A,Z))]


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
    query_params = {param.split('=')[0]: param.split('=')[1] for param in pathname[1:].split('&')}
    A = int(query_params.get('A', None))
    Z = int(query_params.get('Z', None))

    # Call the main_output function to get the DataTable component
    table = main_output(A, Z)

    # Return the DataTable to update the page-content div
    return table

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
   