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
from dash.exceptions import PreventUpdate

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
            # Total de Policiais Militares
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Total de Policiais Militares"),
                                    html.H5("-", id="p-totalpolicia-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-group", style=card_icon), 
                                color="warning",
                                style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                            )])
                    ], width=4),

            # Receita
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
                    ], width=4),

            # Direito a reserva
            dbc.Col([
                dbc.CardGroup([
                    dbc.Card([
                        html.Legend("Direito a reserva"),
                        html.H5("-", id="p-reserva-dashboards"),
                    ], style={"padding-left": "20px", "padding-top": "10px"}),
                    dbc.Card(
                        html.Div(className="fa fa-file", style=card_icon), 
                        color="danger",
                        style={"maxWidth": 75, "height": 100, "margin-left": "-10px"},
                    )])
                ], width=4),
        ], style={"margin": "10px"}),
        
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
        ], style={"margin": "10px"}),
        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"height": "100%", "padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=6),
        ], style={"margin": "10px"}),
    ])



# =========  Callbacks  =========== #
# callback para atualizar total de policiais
@app.callback(
Output("p-totalpolicia-dashboards", "children"),
[Input("store-cadastro", "data")])
def update_dropdown(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = len(df_cadastros)

    return  f"{valor}"

# callback para atualizar total de policiais com direito a reserva
@app.callback(
Output("p-reserva-dashboards", "children"),
[Input("store-cadastro", "data")])
def update_dropdown(data):
    TEMPO_MINIMO_ATIVIDADE_EXCECAO = 10950
    TEMPO_MINIMO_ATIVIDADE = 9125
    DATA_REFORMA = pd.to_datetime('2019-12-17', format='%Y-%m-%d').date()

    df_cadastros = pd.DataFrame(data)
    retirement_conditionals   = pd.to_datetime(df_cadastros['Data_de_Ingresso']).dt.date.apply(lambda x: x > DATA_REFORMA)
    not_others_conditionals   = df_cadastros['Tipo_Tempo_Anterior'].apply(lambda x: x != 'Outros')
    time_in_days_conditionals = df_cadastros['Tempo_em_Dias'].apply(lambda x: x >= TEMPO_MINIMO_ATIVIDADE_EXCECAO)
    time_in_days_conditionals_outros = df_cadastros['Tempo_em_Dias'].apply(lambda x: x >= TEMPO_MINIMO_ATIVIDADE)
    for i in df_cadastros.index:
        if(retirement_conditionals[i]):
            df_cadastros.at[i, 'Direito_a_reserva'] = 'sim'
        elif(not_others_conditionals[i] & time_in_days_conditionals[i]):
            df_cadastros.at[i, 'Direito_a_reserva'] = 'nao'
        elif not not_others_conditionals[i] & time_in_days_conditionals_outros[i]:
            df_cadastros.at[i, 'Direito_a_reserva'] = 'sim'
        else: 
            df_cadastros.at[i, 'Direito_a_reserva'] = 'nao'

        if not retirement_conditionals[i]:
          anos_de_servico =  date.today() - pd.to_datetime(df_cadastros.at[i,'Data_de_Ingresso']).date()
          if anos_de_servico.days > TEMPO_MINIMO_ATIVIDADE_EXCECAO:
            df_cadastros.at[i, 'Direito_a_reserva'] = 'sim'
          else:
             df_cadastros.at[i, 'Direito_a_reserva'] = 'nao'
           

    df_cadastros.to_csv('df_cadastro.csv')

    valor = len(df_cadastros[df_cadastros['Direito_a_reserva'] == 'sim'])
    return  f"{valor}"

# callback para atualizar a media de idade
@app.callback(
Output("p-mediaidade-dashboards", "children"),
[Input("store-cadastro", "data")])
def update_dropdown(data):
    df_cadastros = pd.DataFrame(data)

    valor = df_cadastros['Idade'].mean()

    return  f"{valor:.0f} anos"

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

# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_formacao(data_cadastro, theme):
    df = pd.DataFrame(data_cadastro)
    df_separado_s = pd.DataFrame(df['Tipo_Tempo_Anterior'])
    df_separado_s = df_separado_s.groupby(by='Tipo_Tempo_Anterior')['Tipo_Tempo_Anterior'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Tipo_Tempo_Anterior'])
    df_separado_d.rename(columns={'Tipo_Tempo_Anterior' : 'Quant'}, inplace=True)

    fig = px.pie(df, values=df_separado_d.loc[:,'Quant'], names=df_separado_d.index, hole=.2)
    fig.update_layout(title={'text': "Tipo de tempo anterior"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,255)')
    #pdb.set_trace()              
    return fig

# Gráfico 4
@app.callback(
    Output('graph4', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_formacao(data_cadastro, theme):
    df = pd.DataFrame(data_cadastro)
    df_separado_s = pd.DataFrame(df['Direito_a_reserva'])
    df_separado_s = df_separado_s.groupby(by='Direito_a_reserva')['Direito_a_reserva'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Direito_a_reserva'])
    df_separado_d.rename(columns={'Direito_a_reserva' : 'Quant'}, inplace=True)

    fig = px.pie(df, values=df_separado_d.loc[:,'Quant'], names=df_separado_d.index, hole=.2)
    fig.update_layout(title={'text': "Direito a reserva"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,255)')
    #pdb.set_trace()              
    return fig