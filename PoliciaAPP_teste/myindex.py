from collections.abc import MutableMapping
from dash import html, dcc
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

# import from folders
from app import *
from components import sidebar, dashboards, cadastros

# DataFrames and Dcc.Store

df_cadastro= pd.read_csv("df_cadastro.csv", index_col=0, parse_dates=True)
df_cadastro_aux = df_cadastro.to_dict()

df_cat_sexo= pd.read_csv("df_cat_sexo.csv", index_col=0, parse_dates=True)
df_cat_sexo_aux = df_cat_sexo.to_dict()

df_cat_tipo_sanguineo= pd.read_csv("df_cat_tipo_sanguineo.csv", index_col=0, parse_dates=True)
df_cat_tipo_sanguineo_aux = df_cat_tipo_sanguineo.to_dict()


# =========  Layout  =========== #
content = html.Div(id="page-content")

app.layout = dbc.Container(children=[
    dcc.Store(id='store-cadastro', data=df_cadastro_aux),
    dcc.Store(id='store-cat_sexo', data=df_cat_sexo_aux),
    dcc.Store(id='store-cat_tipo_sanguineo', data=df_cat_tipo_sanguineo_aux),
    
    dbc.Row([
        dbc.Col([
            dcc.Location(id="url"),
            sidebar.layout
        ], md=2),

        dbc.Col([
            html.Div(id="page-content")
        ], md=10),
    ])

], fluid=True, style={"padding": "0px"}, className="dbc")


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/" or pathname == "/dashboards":
        return dashboards.layout

    if pathname == "/cadastros":
        return cadastros.layout
        

if __name__ == '__main__':
    app.run_server(debug=True)