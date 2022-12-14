import dash
from dash.dependencies import Input, Output
from dash import dash_table
from dash.dash_table.Format import Group
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

from app import app
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

# =========  Layout  =========== #
layout = dbc.Col([
    dbc.Row([
        html.Legend("Tabela de Cadastros"),
        html.Div(id="tabela-cadastro", className="dbc"),
    ]),
    
], style={"padding": "10px"})

# =========  Callbacks  =========== #
# Tabela
@app.callback(
    Output('tabela-cadastro', 'children'),
    Input('store-cadastro', 'data')
)
def imprimir_tabela (data):
    df = pd.DataFrame(data)
    df['Data_Nascimento'] = pd.to_datetime(df['Data_Nascimento']).dt.date

    df = df.fillna('-')

    df.sort_values(by='Nome', ascending=False)

    tabela = dash_table.DataTable(
        id='datatable-interactivity',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": False, "hideable": True}
            if i == "Descrição" or i == "Fixo" or i == "Efetuado"
            else {"name": i, "id": i, "deletable": False, "selectable": False}
            for i in df.columns
        ],

        data=df.to_dict('records'),
        filter_action="native",    
        sort_action="native",       
        sort_mode="single",  
        selected_columns=[],        
        selected_rows=[],          
        page_action="native",      
        page_current=0,             
        page_size=10,                        
    ),

    return tabela