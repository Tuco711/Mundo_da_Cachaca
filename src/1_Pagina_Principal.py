import streamlit as st
import pandas as pd

#* Tempo gasto: 12h

#* Como rodar: python -m streamlit run 1_Produtos.py

# Comparativo mensal/quarter/anual entre periodo atual contra os mesmos periodos dos anos anteriores de:
#   Por cliente;
#   Por produto;
#   Total da empresa por clientes e por produtos.

# Colunas:
# A - Numero da Fatura emitida por nós
# B - Se é Fatura (emitimos e o cliente tem tantos dias para pagar), Fatura-recibo (Cliente paga adiantado e 
# já emitimos a fatura que tb é um recibo), Nota de Crédito.. etc
# C - Código do artigo/produto que estamos faturando ao cliente;
# D - Descriçao do artigo/produto 
# E - Numero da conta do cliente com a gente (interno)
# F - Nome do Cliente
# G - Data de emissão da fatura
# H - Preço total dos artigos/produtos (sem IVA)
# I - Valor total do IVA dos artigos/produtos 
# J - Preço total dos artigos/produtos já com IVA
# K - Quantidade do artigo/produto faturado
# L - preço de cada unidade do artigo/produto em questão (sem IVA)

st.set_page_config(layout="wide")
st.title('Mundo da Cachaça')
st.markdown('Dashboard de Vendas')


# Configuração do dataframe / database
try:
    df = pd.read_feather('data/dados.feather')

except Exception as e:
    st.error(f'Erro: {e}')
    df = pd.DataFrame()


# Configuração do arquivo - input
try:
    arquivo = st.file_uploader('Escolha o arquivo CSV ou XLSX', type = ['csv', 'xlsx'])
    
    from_file = arquivo.name


    if arquivo is not None:

        # Importando o arquivo
        if 'csv' in arquivo.name:
            file = pd.read_csv(arquivo, sep=';', decimal=',')

        elif 'xlsx' in arquivo.name:
            file = pd.read_excel(arquivo, sheet_name='docscomerciais.estatisticas')

        else:
            st.error('Formato de arquivo não suportado')

        # Criando o dataframe
        df = pd.concat([df, file], join='outer').reset_index()
    else:
        st.error('Nenhum arquivo selecionado')

# Tratamento dos dados
    df.dropna(axis=0, inplace=True)

    df['Data doc.'].dt.strftime('%d-%m-%Y')
    df['Data doc.'] = pd.to_datetime(df['Data doc.'])

    df['Ano'] = df['Data doc.'].dt.year.astype(int).astype(str)
    df['Mes'] = df['Data doc.'].dt.month.astype(int).astype(str)
    df['Trimestre'] = df['Data doc.'].dt.quarter.astype(int).astype(str)
    df['Semestre'] = (df['Data doc.'].dt.month // 6 + 1).astype(int).astype(str)

    st.session_state['df'] = df


    if not df.empty:
        df.to_feather('data/dados.feather')

    st.session_state['df'] = df 

except Exception as e:
    st.error(f'Erro: {e}')