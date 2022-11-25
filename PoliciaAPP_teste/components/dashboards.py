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

            # PMs afastados
            dbc.Col([
                    dbc.CardGroup([
                            dbc.Card([
                                    html.Legend("Afastados"),
                                    html.H5("-",id="p-afastados-dashboards", style={}),
                            ], style={"padding-left": "20px", "padding-top": "10px"}),
                            dbc.Card(
                                html.Div(className="fa fa-plus-square", style=card_icon), 
                                color="danger",
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
        ], style={"margin": "10px"}),

        dbc.Row([
            dbc.Col([
                dbc.Card([
                        html.Legend("Filtrar ", className="card-title"),
                        html.Label("Categorias a serem filtradas"),
                        html.Div(
                            dcc.Dropdown(
                            id="dropdown-receita",
                            clearable=False,
                            style={"width": "100%"},
                            persistence=True,
                            persistence_type="session",
                            multi=True)                       
                        ),
                        
                        html.Legend("Período de Análise", style={"margin-top": "10px"}),
                        dcc.DatePickerRange(
                            month_format='DD/MM/YYYY',
                            end_date_placeholder_text='Data...',
                            start_date=datetime.today() - timedelta(days=31),
                            end_date=datetime.today(),
                            with_portal=True,
                            updatemode='singledate',
                            id='date-picker-config',
                            style={'z-index': '100'})],

                style={"height": "100%", "padding": "20px"}), 

            ], width=4),

            dbc.Col(dbc.Card(dcc.Graph(id="graph1"), style={"height": "100%", "padding": "10px"}), width=8),
        ], style={"margin": "10px"}),

        dbc.Row([
            dbc.Col(dbc.Card(dcc.Graph(id="graph2"), style={"padding": "10px"}), width=6),
            dbc.Col(dbc.Card(dcc.Graph(id="graph3"), style={"padding": "10px"}), width=3),
            dbc.Col(dbc.Card(dcc.Graph(id="graph4"), style={"padding": "10px"}), width=3),
        ], style={"margin": "10px"})
    ])



# =========  Callbacks  =========== #
# Dropdown Receita
@app.callback([Output("dropdown-receita", "options"),
    Output("dropdown-receita", "value"),
    Output("p-receita-dashboards", "children")],
    Input("store-cadastro", "data"))
def populate_dropdownvalues(data):
    df = pd.DataFrame(data)
    valor = len(df)
    val = df.Categoria.unique().tolist()

    return [([{"label": x, "value": x} for x in df.Categoria.unique()]), val, f"R$ {valor}"]

# VALOR - saldo
@app.callback(
    Output("p-totalpolicia-dashboards", "children"),
    [Input("store-cadastro", "data")])
def total_pms(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = len(df_cadastros)
    
    return f"{valor}"

@app.callback(
    Output("p-afastados-dashboards", "children"),
    [Input("store-cadastro", "data")])
def pms_afastados(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = df_cadastros['Valor'].sum() - df_cadastros['Valor'].sum()

    return f"{valor}" 
@app.callback(
    Output("p-mediaidade-dashboards", "children"),
    [Input("store-cadastro", "data")])
def pms_idade(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = df_cadastros['Valor'].sum() - df_cadastros['Valor'].sum()

    return f"{valor}"

@app.callback(
    Output("p-reserva-dashboards", "children"),
    [Input("store-cadastro", "data")])
def pms_reserva(cadastros):
    df_cadastros = pd.DataFrame(cadastros)

    valor = df_cadastros['Valor'].sum() - df_cadastros['Valor'].sum()

    return f"{valor}"
    
# Gráfico 1
""" @app.callback(
    Output('graph1', 'figure'),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")])
def update_output(data_cadastro, theme):
    df_cadastro = pd.DataFrame(data_cadastro).sort_values(by='Data de Engresso', ascending=True)
    df_ca = df_cadastro.groupby("Data de Engresso").count()

    dfs = [df_ca]

    for df in dfs:
        df['Acumulo'] = len(df)
        df["Data"] = pd.to_datetime(df["Data de Engresso"])
        df["Mes"] = df["Data de Engresso"].apply(lambda x: x.month)

    df_receitas_mes = df_rc.groupby("Mes")["Valor"].sum()
    df_saldo_mes = df_receitas_mes - df_cadastros_mes
    df_saldo_mes.to_frame()
    df_saldo_mes = df_saldo_mes.reset_index()
    df_saldo_mes['Acumulado'] = df_saldo_mes['Valor'].cumsum()
    df_saldo_mes['Mes'] = df['Mes'].apply(lambda x: calendar.month_abbr[x])


    fig = go.Figure()
    
    # fig.add_trace(go.Scatter(name='cadastros', x=df_ds['Data'], y=df_ds['Acumulo'], fill='tonexty', mode='lines'))
    fig.add_trace(go.Scatter(name='Policiais', x=df_rc['Data'], y=df_rc['Acumulo'], fill='tonextx', mode='lines'))
    # fig.add_trace(go.Scatter(name='Saldo Mensal', x=df_saldo_mes['Mes'], y=df_saldo_mes['Acumulado'], mode='lines'))

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig """

# Gráfico 2
""" @app.callback(
    Output('graph2', 'figure'),
    [Input('store-cadastro', 'data'),
    Input('dropdown-receita', 'value'),
    Input('date-picker-config', 'start_date'),
    Input('date-picker-config', 'end_date'), 
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]    
)
def graph2_show(data_cadastro, cadastro, start_date, end_date, theme):
    df_ca = pd.DataFrame(data_cadastro)


    df_ca['Output'] = 'Policiais na ativa'
    df_final = pd.concat(df_ca)

    mask = (df_final['Data'] > start_date) & (df_final['Data'] <= end_date) 
    df_final = df_final.loc[mask]

    df_final = df_final[df_final['Categoria'].isin(cadastro)]

    fig = px.bar(df_final, x="Data", y="Valor", color='Output', barmode="group")        
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig """


# Gráfico 3
@app.callback(
    Output('graph3', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_receita(data_cadastros, theme):
    df = pd.DataFrame(data_cadastros)
    #pdb.set_trace()
    df_separado_s = pd.DataFrame(df['Sexo'])
    df_separado_s = df_separado_s.groupby(by='Sexo')['Sexo'].count()
    df_separado_d = pd.DataFrame(df_separado_s, columns=['Quant'])
    #df_separado_s.to_frame()
    #df_separado_s.rename(columns={0 : 'Quant'}, inplace=True)
    #df_separado_s['Sexo'] = df['Sexo']
    #df_separado_s['Quantidade'] = df.groupby(by='Sexo').count()
    #df_separado = df_separado.groupby(by='Sexo').count()
    #
    #df_separado = df.groupby(by='Sexo').agg('count')
    #pdb.set_trace()

    fig = px.pie(df, values=df_separado_d.loc[:,'Quant'], names=df_separado_d.iloc[:,0], hole=.2)
    fig.update_layout(title={'text': "PMs por sexo"})
    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,255)', plot_bgcolor='rgba(255,0,0,255)')
                  
    return fig    

# Gráfico 4
""" @app.callback(
    Output('graph4', "figure"),
    [Input('store-cadastro', 'data'),
    Input(ThemeChangerAIO.ids.radio("theme"), "value")]
)
def pie_cadastro(data_cadastro, theme):
    df = pd.DataFrame(data_cadastro)
    df = df[df['Sexo']]

    fig = px.pie(df, values=len(df), names=df.Sexo, hole=.2)
    fig.update_layout(title={'text': "PMs por gênero"})

    fig.update_layout(margin=graph_margin, template=template_from_url(theme))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')

    return fig """