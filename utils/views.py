from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import utils.dash_reusable_components as drc


def view():
    return \
    html.Div(id="body", className="container scalable", children=[
        html.Div(id="app-container", children=[
            html.Div(id="left-column", children=[
                drc.Card(id="nuclei-card", children=[
                    drc.NamedInput('N', id='neutron-input', value=None, type="number", min=0, max=200, className="input1", placeholder='Enter Neutron Number'),
                    drc.NamedInput('Z', id='proton-input', value=None, type="number", min=0, max=200, className="input1", placeholder='Enter Proton Number'),
                ]),
                drc.Card(id="button-card", children=[
                    html.Button('Download Samples', id='download-button', className="button1")
                ]),
            ]),
            html.Div(id='center-column', children=[
                dcc.Loading(children=[
                    html.Div(id="div-graphs")
                ])
            ]),
            html.Div(id="right-column", children=[
            ]),                   
        ]),
    ]),
