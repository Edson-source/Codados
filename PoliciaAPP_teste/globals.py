import pandas as pd
import os

# =========  Criação das tabelas  =========== #
if ("df_cadastro.csv" in os.listdir()):
    df_cadastro = pd.read_csv("df_cadastro.csv", index_col=0, parse_dates=True)
    df_cadastro['Data_Nascimento'] = pd.to_datetime(df_cadastro['Data_Nascimento'])
    df_cadastro['Data_de_Ingresso'] = pd.to_datetime(df_cadastro['Data_de_Ingresso'])
    df_cadastro['Inicio_do_Afastamento'] = pd.to_datetime(df_cadastro['Inicio_do_Afastamento'])
    df_cadastro['Fim_do_Afastamento'] = pd.to_datetime(df_cadastro['Fim_do_Afastamento'])
    
    df_cadastro['Data_Nascimento'] = df_cadastro['Data_Nascimento'].apply(lambda x: x.date())
    df_cadastro['Data_de_Ingresso'] = df_cadastro['Data_de_Ingresso'].apply(lambda x: x.date())
    df_cadastro['Inicio_do_Afastamento'] = df_cadastro['Inicio_do_Afastamento'].apply(lambda x: x.date())
    df_cadastro['Fim_do_Afastamento'] = df_cadastro['Fim_do_Afastamento'].apply(lambda x: x.date())

else:
    data_structure = {
        'Nome':[],
        'Matricula':[],
        'CPF':[],
        'Data_Nascimento':[],
        'Idade':[],
        'Sexo':[],
        'Tipo_Sanguíneo':[],
        'Endereço':[],
        'Cidade':[],
        'CEP':[],
        'Telefone':[],
        'Email':[],
        'Idiomas':[],
        'Comportamento':[], 
        'Formação':[],
        'Curso_de_formação':[],
        'Curso_PM':[],
        'Outros_cursos':[],
        'Licenças_Especiais_Acumuladas':[],
        'Lotação':[],
        'Região':[],
        'Batalhão':[],
        'Companhia':[],
        'Pelotão':[],
        'Grupo':[],
        'Tipo_Tempo_Anterior':[],
        'Tempo_em_Dias':[],
        'Tipo_de_Restrição':[],
        'Fim_da_Restrição':[],
        'Data_de_Ingresso':[],
        'Posto':[],
        'Cidade_de_Atuação':[],
        'Tipo_de_Afastamento':[],
        'Inicio_do_Afastamento':[],
        'Fim_do_Afastamento':[],
        'Direito_a_reserva':[],
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