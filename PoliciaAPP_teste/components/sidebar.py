from multiprocessing.sharedctypes import Value
import os
import dash
import json
import plotly.express as px
from dash import html, dcc
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import app
from datetime import datetime, date

import pdb
from dash_bootstrap_templates import ThemeChangerAIO

# ========= DataFrames ========= #
import numpy as np
import pandas as pd
from globals import *


# ========= Layout ========= #
layout = dbc.Card([
                html.H1("POLICIA MILITAR", className="text-primary"),
                html.H5("SANTA CATARINA", className="text-info"),
                html.Hr(),


    # Seção PERFIL ------------------------
                dbc.Button(id='botao_avatar',
                    children=[html.Img(src="/assets/logo.png", id="avatar_change", alt="Avatar", className='perfil_avatar'),
                ], style={'background-color': 'transparent', 'border-color': 'transparent'}),

                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Selecionar Perfil")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/homem1.png", className='perfil_avatar', top=True),
                                    dbc.CardBody([
                                        html.H4("Perfil 1", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil 1. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/mulher.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil 2", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil 2. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar", color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                        dbc.Row([
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/homem2.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Perfil 3", className="card-title"),
                                        html.P(
                                            "Um Card com exemplo do perfil 3. Texto para preencher o espaço",
                                            className="card-text",
                                        ),
                                        dbc.Button("Acessar",  color="warning"),
                                    ]),
                                ]),
                            ], width=6),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardImg(src="/assets/img_plus.png", top=True, className='perfil_avatar'),
                                    dbc.CardBody([
                                        html.H4("Adicionar Novo Perfil", className="card-title"),
                                        html.P(
                                            "Esse projeto é um protótipo, o botão de adicionar um novo perfil esta desativado momentaneamente!",
                                            className="card-text",
                                        ),
                                        dbc.Button("Adicionar", color="success"),
                                    ]),
                                ]),
                            ], width=6),
                        ], style={"padding": "5px"}),
                    ]),
                ],
                style={"background-color": "rgba(0, 0, 0, 0.5)"},
                id="modal-perfil",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True
                ),  

    # Seção + NOVO ------------------------
            dbc.Row([
                dbc.Col([
                    dbc.Button(color="success", id="open-novo-cadastro",
                            children=["Adicionar Cadastro"]),
                ], width=6),

                dbc.Col([
                    dbc.Button(color="danger", id="open-novo-despesa",
                            children=["Apagar Cadastro"]),
                ], width=6)
            ]),


            # Modal Novo cadastro
            html.Div([
                dbc.Modal([
                    dbc.ModalHeader(dbc.ModalTitle("Adicionar novo cadastro")),
                    dbc.ModalBody([
                        dbc.Row([
                            dbc.Col([dbc.Label("Informações pessoais"),])
                       ]),

                        dbc.Row([
                            dbc.Col([
                                    dbc.Label("Nome: "),
                                    dbc.Input(placeholder="Digite nome", id="txt-nome",value=""),
                            ], width=4), 
                            dbc.Col([
                                    dbc.Label("Matricula: "),
                                    dbc.Input(placeholder="123123", id="valor-matricula", value="")
                            ], width=4),
                            dbc.Col([
                                    dbc.Label("Cpf: "),
                                    dbc.Input(placeholder="12345678912", id="valor-cpf", value="")
                            ], width=4)
                        ]),

                        dbc.Row([
                             dbc.Col([
                                dbc.Label("Data de Nascimento: "),
                                dcc.DatePickerSingle(id='date-nascimento',
                                    min_date_allowed=date(1800, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={"width": "100%"}
                                ),
                            ], width=4),

                            dbc.Col([
                                    dbc.Label("Sexo: "),
                                    dbc.Select(id='select-sexo', 
                                    options=[{'label': i, 'value': i} for i in df_cat_sexo],
                                    value="",
                                    ),

                            ],width=4),

                             dbc.Col([
                                    dbc.Label("Tipo Sanguineo: "),
                                    dbc.Select(id='tipo-sanguineo', 
                                    options=[{'label': i, 'value': i} for i in df_cat_tipo_sanguineo],
                                    value="",
                                    ),
                                    

                            ],width=4),                           
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Endereço: "),
                                 dbc.Input(placeholder="Digite aqui", id="txt-endereco", value="")
                            ], width=4),

                             dbc.Col([
                                    dbc.Label("Cidade: "),
                                    dbc.Input(placeholder="Digite aqui", id="txt-cidade", value="")
                            ],width=4),
                            dbc.Col([
                                    dbc.Label("CEP: "),
                                    dbc.Input(placeholder="Digite aqui", id="txt-cep", value="")
                            ],width=4),
                        ]),

                        dbc.Row([
                            dbc.Col([
                                dbc.Label("Telefone: "),
                                dbc.Input(placeholder="Digite o numero com dd", id="txt-telefone", value="")
                            ],width=4),

                            dbc.Col([
                                dbc.Label("Email: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-email", value="")
                            ],width=4),

                            dbc.Col([
                                dbc.Label("Idiomas: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-idiomas", value="")
                            ],width=4),
                       ]),

                       dbc.Row([
                        dbc.Col([
                                dbc.Label("Comportamento: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-comportamento", value="")
                            ],width=4),
                          
                        dbc.Col([
                                dbc.Label("Formação: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-formacao", value="")
                            ],width=4),   

                        dbc.Col([
                                dbc.Label("Cursos de Formação:"),
                                dbc.Input(placeholder="Digite aqui", id="txt-curso-formacao", value="")
                            ],width=4),
  
                       ]),

                       dbc.Row([
                        dbc.Col([
                                dbc.Label("Cursos PM: "),
                                dbc.Input(placeholder="Ex: PROERD.. ", id="txt-cursos-pm", value="")
                            ],width=4),
                          
                        dbc.Col([
                                dbc.Label("outros cursos: "),
                                dbc.Input(placeholder="Ex: Libras..", id="txt-outos-cursos", value="")
                            ],width=4),   

                        dbc.Col([
                                dbc.Label("Licenças especiais acumuladas:"),
                                dbc.Input(placeholder="Digite aqui", id="txt-lincenca-esp-acumu", value="")
                            ],width=4),
  
                       ]),

                       dbc.Row([
                            dbc.Col([dbc.Label("Lotação "),])
                       ]),

                       dbc.Row([
                            dbc.Col([
                                dbc.Label("Região:"),
                                dbc.Input(placeholder="Digite aqui", id="txt-regiao", value="")
                            ],width=3),

                            dbc.Col([
                                dbc.Label("Batalhão: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-batalhao", value="")
                            ],width=2),

                            dbc.Col([
                                dbc.Label("Companha: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-companhia", value="")
                            ],width=3),
                           
                            dbc.Col([
                                dbc.Label("Pelotão: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-pelotao", value="")
                            ],width=2),
                          
                            dbc.Col([
                                dbc.Label("Grupo: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-grupo", value="")
                            ],width=2),
                       ]),
                            
                        dbc.Row([
                            dbc.Col([dbc.Label("Tempo Anterior: "),]),
                            dbc.Col([dbc.Label("                "),]),
                            dbc.Col([dbc.Label("Restrição:    "),])
                            
                       ]),
                       
                       dbc.Row([
                        dbc.Col([
                                dbc.Label("Tipo: "),
                                dbc.Input(placeholder="Ex: privado,público ...", id="txt-tipo-temp-ant", value="")
                            ],width=3),
                          
                        dbc.Col([
                                dbc.Label("Tempo em dias: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-tempoemdias", value="")
                            ],width=2),   

                        dbc.Col([dbc.Label("                "),]),

                        dbc.Col([
                                dbc.Label("Tipo: "),
                                dbc.Input(placeholder="Ex: atividade física, serviço externo ...", id="txt-tipo-restricao", value="")
                            ],width=3),

                        dbc.Col([
                                dbc.Label("Fim: "),
                                dbc.Input(placeholder="Digite aqui", id="txt-fim-restricao", value="")
                            ],width=2),   
                       ]),
                       
                         dbc.Row([
                              dbc.Col([
                                dbc.Label("Data de ingresso: "),
                                dcc.DatePickerSingle(id='date-ingresso',
                                    min_date_allowed=date(1800, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={"width": "100%"}
                                ),
                            ], width=4),
                          
                            dbc.Col([
                                    dbc.Label("Posto/Graduação: "),
                                    dbc.Input(placeholder="Digite aqui", id="txt-posto-graduacao", value="")
                            ],width=4),   

                            dbc.Col([
                                    dbc.Label("Cidade de atuação: "),
                                    dbc.Input(placeholder="Digite aqui", id="txt-cidade-atuacao", value="")
                            ],width=4),   
                        ]),  

                         dbc.Row([
                            dbc.Col([dbc.Label("Afastamento: "),]), 
                       ]),

                       dbc.Row([
                              dbc.Col([
                                    dbc.Label("tipo: "),
                                    dbc.Input(placeholder="Digite aqui", id="txt-tipo-afastamento", value="")
                            ],width=4),

                              dbc.Col([
                                dbc.Label("Inicio: "),
                                dcc.DatePickerSingle(id='date-inicio-afastamento',
                                    min_date_allowed=date(1800, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={"width": "100%"}
                                ),
                            ], width=4),

                            dbc.Col([
                                dbc.Label("Fim: "),
                                dcc.DatePickerSingle(id='date-fim-afastamento',
                                    min_date_allowed=date(1800, 1, 1),
                                    max_date_allowed=date(2030, 12, 31),
                                    date=datetime.today(),
                                    style={"width": "100%"}
                                ),
                            ], width=4),
                            dbc.ModalFooter([
                                        dbc.Button("Adicionar Cadastrp", id="salvar_cadastro", color="success"),
                                        dbc.Popover(dbc.PopoverBody("Cadastro salvo"), target="salvar_cadastro", placement="left", trigger="click"),
                                        ])
                        ]),  

                    ])
                ],
                style={"background-color": "rgba(17, 140, 79, 0.05)"},
                id="modal-novo-cadastro",
                size="lg",
                is_open=False,
                centered=True,
                backdrop=True)
            ]),



            ### Modal Apagar Cadastro###
            dbc.Modal([
                dbc.ModalHeader(dbc.ModalTitle("Apagar Cadastro")),
                dbc.ModalBody([
                    dbc.Row([
                        dbc.Col([
                                dbc.Label("Nome: "),
                                dbc.Input(placeholder="Digite o nome", id="txt-matricula-apagar"),
                        ], width=6), 
                        dbc.Col([
                                dbc.Label("Matricula: "),
                                dbc.Input(placeholder="Digite a matricula", id="valor_matricula_apagar", value=""),
                        dbc.ModalFooter([
                                        dbc.Button("Apagar cadastro", id="apagar-cadastro", color="warning"),
                                        dbc.Popover(dbc.PopoverBody("Cadastro Apagado"), target="apagar-cadastro", placement="left", trigger="click"),
                                        ])
                        ], width=6)
                    ]),                    
                ]),
            ],
            style={"background-color": "rgba(17, 140, 79, 0.05)"},
            id="modal-novo-despesa",
            size="lg",
            is_open=False,
            centered=True,
            backdrop=True),
        
# Seção NAV ------------------------
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink("Dashboard", href="/dashboards", active="exact"),
                    dbc.NavLink("Cadastros", href="/cadastros", active="exact"),
                ], vertical=True, pills=True, id='nav_buttons', style={"margin-bottom": "50px"}),
            ThemeChangerAIO(aio_id="theme", radio_props={"value":dbc.themes.VAPOR})

        ], id='sidebar_completa'
    )




# =========  Callbacks  =========== #
# Pop-up receita
@app.callback(
    Output("modal-novo-cadastro", "is_open"),
    Input("open-novo-cadastro", "n_clicks"),
    State("modal-novo-cadastro", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Pop-up despesa
@app.callback(
    Output("modal-novo-despesa", "is_open"),
    Input("open-novo-despesa", "n_clicks"),
    State("modal-novo-despesa", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Pop-up perfis
@app.callback(
    Output("modal-perfil", "is_open"),
    Input("botao_avatar", "n_clicks"),
    State("modal-perfil", "is_open")
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open


# Enviar Form receita
@app.callback(
   
    Output('store-cadastro', 'data'),

    Input('salvar_cadastro', 'n_clicks'),
    [
        State("txt-nome", "value"),
        State('valor-matricula', 'value'),
        State('valor-cpf', 'value'),
        State('date-nascimento', 'date'),
        State('select-sexo', 'value'),
        State('tipo-sanguineo', 'value'),
        State('txt-endereco', 'value'),
        State('txt-telefone', 'value'),
        State('txt-email', 'value'),
        State('txt-cidade', 'value'),
        State('txt-cep', 'value'),
        State('txt-idiomas', 'value'),
        State('txt-comportamento', 'value'),
        State('txt-formacao', 'value'),
        State('txt-curso-formacao', 'value'),
        State('txt-cursos-pm', 'value'),
        State('txt-outros-cursos', 'value'),
        State('txt-licenca-esp-acumu', 'value'),
        State('txt-regiao','value'),
        State('txt-batalhao','value'),
        State('txt-companhia','value'),
        State('txt-pelotao','value'),
        State('txt-grupo','value'),
        State('txt-tipo-temp-ant','value'),
        State('txt-tempoemdias','value'),
        State('txt-tipo-restricao','value'),
        State('txt-fim-restricao','value'),
        State('date-ingresso','date'),
        State('txt-posto-graduacao','value'),
        State('txt-cidade-atuacao','value'),
        State('txt-tipo-afastamento','value'),
        State('date-inicio-afastamento','date'),
        State('date-fim-afastamento','date'),
        State('store-cadastro', 'data')
    ], 
)

def salve_from_cadastro(n, nome, matricula, cpf, data_nascimento, sexo, tipo_sanguineo, endereco, telefone, email, cidade, cep, idiomas, comportamento, formacao, curso_formacao, cursos_pm, outros_cursos, licenca_esp_acumu, regiao, batalhao, companhia, pelotao, grupo, tipo_temp_ant, tempoemdias, tipo_restricao, fim_restricao, data_ingresso, posto_graduacao, cidade_atuacao, tipo_afastamento, inicio_afastamento, fim_afastamento, dict_cadastro):
    df_cadastro = pd.DataFrame(dict_cadastro)

    if n and not(nome=="" or nome== None):
        data_nascimento = pd.to_datetime(date).date()
        data_ingresso = pd.to_datetime(date).date()
        inicio_afastamento = pd.to_datetime(date).date()
        fim_afastamento = pd.to_datetime(date).date()
        fim_restricao = pd.to_datetime(date).date()

        tipo_sanguineo = tipo_sanguineo[0] 
        sexo = sexo[0]

        df_cadastro.loc[df_cadastro.shape[0]] = [nome, matricula, cpf, data_nascimento, sexo, tipo_sanguineo, endereco, telefone, email, cidade, cep, idiomas, comportamento, formacao, curso_formacao, cursos_pm, outros_cursos, licenca_esp_acumu, regiao, batalhao, companhia, pelotao, grupo, tipo_temp_ant, tempoemdias, tipo_restricao, fim_restricao, data_ingresso, posto_graduacao, cidade_atuacao, tipo_afastamento, inicio_afastamento, fim_afastamento]
        df_cadastro.to_csv('df_cadastro.csv')

        data_return1 = df_cadastro.to_dict()
    
    return data_return1