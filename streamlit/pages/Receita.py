import streamlit as st  # Importa el módulo streamlit para crear aplicaciones web interactivas
import pandas as pd  # Importa el módulo pandas para manipulación y análisis de datos

top_k = 10

# Define el nombre del archivo de entrada que contiene los datos
#input_file_name = '../data/Receita_2024.csv'
# Lee el archivo CSV y lo carga en un DataFrame de pandas
#df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

# Establece el título de la aplicación web
st.title("TCE PB - Receita (2024)")

def convert_float(value):
    try:
        new_value = str(value)
        new_value = new_value.replace(',', '.')
        new_value = float(new_value)
        return new_value
    except:
        return value

# Upload do arquivo
input_file_name = st.file_uploader("Escolha um arquivo CSV", type="csv")

# Verifica se um arquivo foi carregado
if input_file_name is not None:
    # Carrega o arquivo CSV em um DataFrame
    df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

    column_analysis = 'valor_receita'
    df[column_analysis] = df[column_analysis].apply(lambda x: convert_float(x))

    global_mean = df[column_analysis].mean()

    map_text = {
        'poder': f'Top {top_k} valores por tipo de Poder em relação a média',
        'tipo_lancamento': f'Top {top_k} valores por Tipo de Lançamento em relação a média',
        'ente': f'Top {top_k} valores por Ente em relação a média',
        'cod_unidade_gestora': f'Top {top_k} Código da Unidade Gestora de Licitação por Ente em relação a média'}

    for column in list(map_text.keys()):
        df_top = df.groupby(column)[column_analysis].mean()
        df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
        df_top[column_analysis] = round(df_top[column_analysis], 2)
        df_top['Proporção'] = round(df_top[column_analysis]/global_mean, 1)
        st.text(map_text[column])
        st.dataframe(df_top)
