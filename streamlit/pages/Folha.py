import streamlit as st  # Importa el módulo streamlit para crear aplicaciones web interactivas
import pandas as pd  # Importa el módulo pandas para manipulación y análisis de datos

top_k = 10

# Define el nombre del archivo de entrada que contiene los datos
#input_file_name = '../data/Folha_2024.csv'
# Lee el archivo CSV y lo carga en un DataFrame de pandas
#df = pd.read_csv(input_file_name, sep=';')

# Establece el título de la aplicación web
st.title("TCE PB - Folha de Pagamento")

# Upload do arquivo
input_file_name = st.file_uploader("Escolha um arquivo CSV", type="csv")
# Verifica se um arquivo foi carregado
if input_file_name is not None:
    # Carrega o arquivo CSV em um DataFrame
    df = pd.read_csv(input_file_name, sep=';')

    global_mean = df['valor_remuneracao_total'].mean()
    df_top = df.groupby('cpf_servidor')['valor_remuneracao_total'].mean()
    df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
    df_top['valor_remuneracao_total'] = round(df_top['valor_remuneracao_total'], 2)
    df_top['Proporção'] = round(df_top['valor_remuneracao_total']/global_mean, 1)
    df_top.columns = ['CPF', 'Salário Médio Mensal (em R$)', 'Comparação com a média']

    st.text("O salário médio na Paraíba é de R${:.2f}.".format(global_mean))
    st.text("Estes são os servidores com os maiores salários médios:")
    st.dataframe(df_top)



    df_top = df.groupby('cargo')['valor_remuneracao_total'].mean()
    df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
    df_top['valor_remuneracao_total'] = round(df_top['valor_remuneracao_total'], 2)
    df_top.columns = ['Cargo', 'Salário Médio Mensal (em R$)']
    st.text(f"Estes são os {top_k} cargos com os maiores salários médios:")
    st.dataframe(df_top)



    df_top = df.groupby('vinculo')['valor_remuneracao_total'].mean()
    df_top = pd.DataFrame(df_top.nlargest(top_k).reset_index())
    df_top['valor_remuneracao_total'] = round(df_top['valor_remuneracao_total'], 2)
    df_top.columns = ['Vínculos', 'Salário Médio Mensal (em R$)']
    st.text(f"Estes são os {top_k} vínculos com os maiores salários médios:")
    st.dataframe(df_top)


    st.text("Salário Médio por Poder:")
    df_poder = df.groupby('poder')['valor_remuneracao_total'].mean().reset_index()
    df_poder.sort_values('valor_remuneracao_total', ascending=False, inplace=True)
    df_poder.reset_index(drop=True, inplace=True)
    df_poder['valor_remuneracao_total'] = round(df_poder['valor_remuneracao_total'], 2)
    df_poder.columns = ['Poder', 'Salário Médio Mensal (R$)']
    st.dataframe(df_poder)



    st.text("Salário Médio por Esfera:")
    df_poder = df.groupby('esfera')['valor_remuneracao_total'].mean().reset_index()
    df_poder.sort_values('valor_remuneracao_total', ascending=False, inplace=True)
    df_poder.reset_index(drop=True, inplace=True)
    df_poder['valor_remuneracao_total'] = round(df_poder['valor_remuneracao_total'], 2)
    df_poder.columns = ['Esfera', 'Salário Médio Mensal (R$)']
    st.dataframe(df_poder)



    # Crea una entrada de texto en la aplicación web para que el usuario ingrese su búsqueda
    text = st.text_input("Digite o CPF do funcionário.")
    df_filtered = df[df['cpf_servidor'].apply(lambda x: True if text in str(x) else False)]
    # Muestra el DataFrame filtrado en la aplicación web
    st.dataframe(df_filtered)
    cpf_test = df_filtered[df_filtered['cpf_servidor'].apply(lambda x: True if text in str(x) else False)]
    cpf_test = cpf_test.groupby('data')['valor_remuneracao_total'].sum().reset_index()
    st.line_chart(cpf_test, x='data', y='valor_remuneracao_total')

    # Pagamento médio mensal/anbual por folha de pagamento (orgao)