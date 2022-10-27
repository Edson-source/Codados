import pandas as pd
import os

# =========  Criação das tabelas  =========== #
if ("df_cadastro.csv" in os.listdir()):
    df_cadastro = pd.read_csv("df_cadastro.csv", index_col=0, parse_dates=True)

else:
    data_structure = {
        'Nome':[],
        'Matricula':[],
        'CPF':[],
        'Data Nascimento':[],
        'Sexo':[],
        'Tipo Sanguíneo':[],
        'Telefone':[],
        'Email':[],
        'Endereço':[],
        'Cidade':[],
        'CEP':[],
        'Idiomas':[],
        'Comportamento':[],  
        'Formação':[],
        'Curso de formação':[],
        'Curso PM':[],
        'Outros cursos':[],
        'Licenças Especiais Acumuladas':[],
        'Região':[],
        'Batalhão':[],
        'Companhia':[],
        'Pelotão':[],
        'Grupo':[],
        'Tipo Tempo Anterior':[],
        'Tempo em Dias':[],
        'Tipo de Restrição':[],
        'Fim da Restrição':[],
        'Data de Engresso':[],
        'Posto':[],
        'Cidade de Atuação':[],
        'Tipo de Afastamento':[],
        'Inicio do Afastamento':[],
        'Fim do Afastamento':[],                            
        }

    df_cadastro = pd.DataFrame(data_structure)
    df_cadastro.to_csv("df_cadastro.csv")

if ("df_cat_sexo.csv" in os.listdir()) and ("df_cat_tipo_sanguineo.csv" in os.listdir()):
    df_cat_sexo = pd.read_csv("df_cat_sexo.csv", index_col=0)
    df_cat_tipo_sanguineo = pd.read_csv("df_cat_tipo_sanguineo.csv", index_col=0)
    df_cat_sexo = df_cat_sexo.values.tolist()
    df_cat_tipo_sanguineo = df_cat_tipo_sanguineo.values.tolist()

else:    
    df_cat_sexo = {'Sexo': ["Masculino", "Feminino"]}
    df_cat_tipo_sanguineo = {'Tipo Sanguineo': ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]}
    
    df_cat_sexo = pd.DataFrame(df_cat_sexo, columns=['Sexo'])
    df_cat_tipo_sanguineo = pd.DataFrame(df_cat_tipo_sanguineo, columns=['Tipo Sanguineo'])
    df_cat_sexo.to_csv("df_cat_sexo.csv")
    df_cat_tipo_sanguineo.to_csv("df_cat_tipo_sanguineo.csv")