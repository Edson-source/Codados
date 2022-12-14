from dash import html, dcc
from dash.dependencies import Input, Output, State
from datetime import date, datetime, timedelta
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import calendar
from globals import *
from app import app

import pdb
from dash_bootstrap_templates import template_from_url, ThemeChangerAIO

card_icon = {
    "color": "white",
    "textAlign": "center",
    "fontSize": 30,
    "margin": "auto",
}

graph_margin=dict(l=25, r=25, t=25, b=0)


# =========  Layout  =========== #
layout = dbc.Col([
        dbc.Row([
            # total de PMs
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([

                                    html.Legend("Total de PMs"),
                                    html.H5("-",id="p-totalpolicia-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-group", style=card_icon), 
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=3),


            # Média de Idade
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Média de Idade"),
                                    html.H5('-', id="p-mediaidade-dashboards"),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-id-card", style=card_icon), 
                                color="success",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=3),

            # Reserva
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Direito a reserva"),
                        html.H5("-", id="p-reserva-dashboards"),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-file", style=card_icon), 
                        color="warning",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                    )])
                ], width=3),
        ], style={"margin": "10px", "font-size" : "12px"}),

        dbc.Row([
            #dbc.Col([
                    #dbc.Card([
                            #html.Legend("Filtrar ", className="card-title"),
                            #html.Label("Categorias a serem filtradas"),
                            #html.Div(
                                #dcc.Dropdown(
                                #id="dropdown-receita",
                                #clearable=False,
                                #style={"width": "100%"},
                                #persistence=True,
                                #persistence_type="session",
                                #multi=True)                       
                            #),
                            
                            #html.Legend("Período de Análise", style={"margin-top": "10px"}),
                            #dcc.DatePickerRange(
                                #month_format='DD/MM/YYYY',
                                #end_date_placeholder_text='Data...',
                                #start_date=datetime.today() - timedelta(days=31),
                                #end_date=datetime.today(),
                                #with_portal=True,
                                #updatemode='singledate',
                                #id='date-picker-config',
                                #style={'z-index': '100'})],

                    #style={"height": "100%", "padding": "20px"}), 

            #], width=4), 

            dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
        ], style={"margin": "10px"}),

    ])



# =========  Callbacks  =========== #
# Total de PMs
@app.callback(
    Output("p-totalpolicia-dashboards", "children"),
    [Input("store-cadastro", "data")])
def total_pms(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = len(df_cadastros)
    
    return f"{valor}"

@app.callback(
    Output("p-mediaidade-dashboards", "children"),
    [Input("store-cadastro", "data")])
def pms_idade(cadastros):
    df = pd.DataFrame(cadastros)

    df_separado_s = pd.DataFrame(df['Idade'])
    soma = df_separado_s['Idade'].sum()
    media = soma / len(df)

    return f"{media} anos"

@app.callback(
    Output("p-reserva-dashboards", "children"),
    [Input("store-cadastro", "data")])
def pms_reserva(cadastros):
    df = pd.DataFrame(cadastros)
    df_separado_s = pd.DataFrame(df['Direito_a_reserva'])
    df_separado_s = df_separado_s.groupby(by='Direito_a_reserva')['Direito_a_reserva'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Direito_a_reserva'])
    df_separado_d.rename(columns={'Direito_a_reserva' : 'Quant'}, inplace=True)

    return f"{df_separado_d.loc['sim','Quant']}"
    


# Gráfico 1
@app.callback(
    Output('graph1', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_genero(data_cadastros, theme):
    df = pd.DataFrame(data_cadastros)
    df_separado_s = pd.DataFrame(df['Sexo'])
    df_separado_s = df_separado_s.groupby(by='Sexo')['Sexo'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Sexo'])
    df_separado_d.rename(columns={'Sexo' : 'Quant'}, inplace=True)

    fig = px.pie(df, values=df_separado_d.loc[:,'Quant'], names=df_separado_d.index, hole=.2)
    fig.update_layout(title={'text': "PMs por sexo"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,255)')
    #pdb.set_trace()              
    return fig    

# Gráfico 2
@app.callback(
    Output('graph2', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_formacao(data_cadastro, theme):
    df = pd.DataFrame(data_cadastro)
    df_separado_s = pd.DataFrame(df['Posto'])
    df_separado_s = df_separado_s.groupby(by='Posto')['Posto'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Posto'])
    df_separado_d.rename(columns={'Posto' : 'Quant'}, inplace=True)

    fig = px.pie(df, values=df_separado_d.loc[:,'Quant'], names=df_separado_d.index, hole=.2)
    fig.update_layout(title={'text': "PMs por Posto/Graduação"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,255)')
    #pdb.set_trace()              
    return fig  