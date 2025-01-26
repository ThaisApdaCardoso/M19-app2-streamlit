# -*- coding: utf-8 -*-

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Configurações iniciais
def setup_page():
    st.set_page_config(page_title="Streamlit Parte 2 App", layout="wide")
    st.title("Streamlit Parte 2 - Aplicativo Completo")

def load_dataset():
    # Carregar o dataset enviado pelo usuário
    bank = pd.read_csv('bank-additional-full.csv', sep=';')
    bank.head(10)
    
def main():
    setup_page()

    st.header("Aula 1: Apresentação do Dataset")
    bank = load_dataset()
    st.write("Dataset Exemplo:", bank)

    st.header("Aula 2: Ferramentas de Filtros e Visualização")

    st.subheader("Parte 1: 1 Coluna como Filtro")
    column_filter = st.selectbox("Selecione uma coluna para visualizar", bank.columns)
    st.write(bank[[column_filter]])

    st.slider("Selecione um valor para filtro", min_value=float(bank[column_filter].min()), max_value=float(bank[column_filter].max()))

    fig, ax = plt.subplots()
    sns.histplot(bank[column_filter], ax=ax)
    st.pyplot(fig)

    st.subheader("Parte 2: 2 Colunas como Filtro")
    columns_filter = st.multiselect("Selecione colunas para visualizar", bank.columns)
    st.write(bank[columns_filter])

    st.subheader("Parte 3: Formulário de Entrada")
    with st.form("input_form"):
        name = st.text_input("Nome")
        value = st.number_input("Valor", min_value=0, max_value=100, step=1)
        submitted = st.form_submit_button("Enviar")
        if submitted:
            st.success(f"Enviado! Nome: {name}, Valor: {value}")

    sns.set_theme()

    st.header("Aula 3: 9 Colunas como Filtro")
    filters = {}
    cols = st.columns(9)
    for i, col in enumerate(cols):
        if i < len(bank.columns):
            filters[bank.columns[i]] = col.selectbox(f"Filtro para {bank.columns[i]}", options=bank[bank.columns[i]].unique())
    st.write(filters)

    st.header("Aula 4: Cache e Atualizações")
    st.cache()
    st.write("Cache aplicado com sucesso!")

    st.header("Aula 5: Upload de Arquivo")
    uploaded_file = st.file_uploader("Faça o upload do seu arquivo")
    if uploaded_file:
        user_df = pd.read_csv(uploaded_file)
        st.write(user_df)

    st.header("Aula 6: Download de Arquivo")
    csv = bank.to_csv(index=False).encode('utf-8')
    st.download_button("Baixar CSV", csv, "dataset.csv")

    st.header("Aula 7: Layout com Colunas e Botões")
    col1, col2 = st.columns(2)
    with col1:
        st.radio("Opção 1", ["A", "B", "C"])
    with col2:
        st.radio("Opção 2", ["X", "Y", "Z"])

if __name__ == "__main__":
    main()
