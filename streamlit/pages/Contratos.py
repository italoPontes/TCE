import streamlit as st  # Importa el módulo streamlit para crear aplicaciones web interactivas
import pandas as pd  # Importa el módulo pandas para manipulación y análisis de datos

top_k = 10

# Establece el título de la aplicación web
st.title("TCE PB - Contratos (2024)")

def convert_float(value):
    try:
        new_value = str(value)
        new_value = new_value.replace(',', '.')
        new_value = float(new_value)
        return new_value
    except:
        return value
    
# Define el nombre del archivo de entrada que contiene los datos
#input_file_name = '../data/Contratos_2024.csv'
# Lee el archivo CSV y lo carga en un DataFrame de pandas
#df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

# Upload do arquivo
input_file_name = st.file_uploader("Escolha um arquivo CSV", type="csv")
# Verifica se um arquivo foi carregado
if input_file_name is not None:
    # Carrega o arquivo CSV em um DataFrame
    df = pd.read_csv(input_file_name, sep=';', encoding='latin-1')

    for column_analysis in ['valor_contratado', 'valor_proposta']:
        df[column_analysis] = df[column_analysis].apply(lambda x: convert_float(x))

    global_mean = df[column_analysis].mean()

    map_text = {
        'cpf_cnpj_licitante': f'Top {top_k} valores por CPF/CNPJ Licitante em relação a média',
        'numero_licitacao': f'Top {top_k} valores por Número de Licitação em relação a média',
        'ente': f'Top {top_k} valores por Ente em relação a média',
        'cod_modalidade_licitacao': f'Top {top_k} Código Modalidade de Licitação por Ente em relação a média'}

    for column in list(map_text.keys()):
        df_top = df.groupby(column)[column_analysis].mean()
        df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
        df_top[column_analysis] = round(df_top[column_analysis], 2)
        df_top['Proporção'] = round(df_top[column_analysis]/global_mean, 1)
        st.text(map_text[column])
        st.dataframe(df_top)


    st.title('Top Discrepância: Contratado - Proposta (valor absoluto)')
    valor1 = 'valor_contratado'
    valor2 = 'valor_proposta'
    df['Discrepancia'] = df[valor1] - df[valor2]
    df_top = df.nlargest(10, 'Discrepancia')
    df_top = pd.melt(df_top, id_vars=['unidade_gestora'],
                            value_vars=[valor1,
                                        valor2])
    df_top.columns = ['Unidade_Gestora', 'Tipo Pagamento', 'Valor']
    st.bar_chart(df_top, x="Unidade_Gestora",
                        y="Valor",
                        color="Tipo Pagamento", stack=False)


    st.title('Top Discrepância: Contratado - Proposta (valor relativo)')
    df['Discrepancia Relativa'] = df['Discrepancia']/df[valor1]
    df_top_r = df.nlargest(10, 'Discrepancia Relativa')
    df_top_r = pd.melt(df_top_r, id_vars=['unidade_gestora'],
                            value_vars=[valor1,
                                        valor2])
    df_top_r.columns = ['Unidade_Gestora', 'Tipo Pagamento', 'Valor']
    st.bar_chart(df_top_r, x="Unidade_Gestora",
                        y="Valor",
                        color="Tipo Pagamento", stack=False)


    st.title('Top Discrepância: Busca por Ente')
    feat = 'ente'
    data = 'data_publicacao'
    valor = 'valor_contratado'
    text = st.text_input("Digite os Ente a serem analisados:.")
    text = [word.lower() for word in text.split(',')]   
    df_agg = df[df[feat].apply(lambda x: True if x.lower() in text else False)]
    df_agg = df_agg.groupby([data, feat])[valor].sum().reset_index()
    st.line_chart(df_agg, x=data, y=valor, color=feat)