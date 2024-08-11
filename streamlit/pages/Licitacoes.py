import streamlit as st  # Importa el módulo streamlit para crear aplicaciones web interactivas
import pandas as pd  # Importa el módulo pandas para manipulación y análisis de datos

# Define el nombre del archivo de entrada que contiene los datos
input_file_name = 'data/Licitacoes_2024.csv'

# Lee el archivo CSV y lo carga en un DataFrame de pandas
df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

# Establece el título de la aplicación web
st.title("TCE PB - Licitações (2024)")

def convert_float(value):
    try:
        new_value = str(value)
        new_value = new_value.replace(',', '.')
        new_value = float(new_value)
        return new_value
    except:
        return value

for column in ['valor_proposta', 'valor_homologacao',
               'valor_empenhado', 'valor_pago']:
    df[column] = df[column].apply(lambda x: convert_float(x))

top_k = 10

column_analysis = 'valor_homologacao'
global_mean = df[column_analysis].mean()

map_text = {
    'numero_licitacao': f'Top {top_k} valores por Número de Licitação em relação a média',
    'ente': f'Top {top_k} valores por Ente em relação a média',
    'unidade_gestora': f'Top {top_k} valores por Unidade Gestora em relação a média'}

for column in ['numero_licitacao', 'ente', 'unidade_gestora']:    
    df_top = df.groupby(column)[column_analysis].mean()
    df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
    df_top[column_analysis] = round(df_top[column_analysis], 2)
    df_top['Proporção'] = round(df_top[column_analysis]/global_mean, 1)
    st.text(map_text[column])
    st.dataframe(df_top)

