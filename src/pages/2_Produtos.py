import streamlit as st
import pandas as pd
import plotly.express as px

#* Tempo gasto: 10h

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


# Configuração da página
st.set_page_config(layout="wide")
st.title('Mundo da Cachaça')
st.markdown('Dashboard de Vendas')


# df = pd.read_feather('data/dados.feather')
df = st.session_state['df']
    

# if arquivo is not None:

#     # Importando o arquivo
#     if 'csv' in arquivo.name:
#         file = pd.read_csv(arquivo, sep=';', decimal=',')

#     elif 'xlsx' in arquivo.name:
#         file = pd.read_excel(arquivo, sheet_name='docscomerciais.estatisticas')

#     else:
#         st.error('Formato de arquivo não suportado')

#     # Criando o dataframe
#     df = pd.concat([df, file], ignore_index=True)
# else:
#     st.error('Nenhum arquivo selecionado')

# if df.empty:
#     st.stop()


# # Tratamento dos dados
# df.dropna(axis=0, inplace=True)

# df['Data doc.'].dt.strftime('%d-%m-%Y')
# df['Data doc.'] = pd.to_datetime(df['Data doc.'])

# df['Ano'] = df['Data doc.'].dt.year.astype(int).astype(str)
# df['Mes'] = df['Data doc.'].dt.month.astype(int).astype(str)
# df['Trimestre'] = df['Data doc.'].dt.quarter.astype(int).astype(str)
# df['Semestre'] = (df['Data doc.'].dt.month // 6 + 1).astype(int).astype(str)

# Sidebar
st.sidebar.title('Filtros')
opcao = st.sidebar.selectbox('Periodo de Tempo', ['Ano', 'Trimestre', 'Semestre', 'Mês'])

# Selecionando o periodo
match opcao:
    case 'Ano':
        df['Periodo'] = df['Ano']
    case 'Trimestre':
        df['Periodo'] = df['Trimestre']
    case 'Semestre':
        df['Periodo'] = df['Semestre']
    case 'Mês':
        df['Periodo'] = df['Mes']

df['Periodo'] = df['Periodo'].astype(str)
periodo = st.sidebar.selectbox('Selecione o periodo', df['Periodo'].unique())

df_filtered = df[df['Periodo'] == periodo]

# Dados do timestamp escolhido
st.write(f'Dados do periodo escolhido: {opcao} - {periodo}')
col1, col2 = st.columns(2)

# Grupo por Cliente/Produto/Receita Liquida
gasto_cliente_produto = df_filtered.groupby(['Nome', 'Nome Artigo'])[['Liquido Mov.']].sum().reset_index()
rounder = lambda x: round(x, 2)
gasto_cliente_produto['Liquido Mov.'] = gasto_cliente_produto['Liquido Mov.'].apply(rounder)

gasto_cliente_produto = gasto_cliente_produto.sort_values('Liquido Mov.', ascending=False)

# Faturamento por Cliente/Produto
fig_cliente = px.bar(gasto_cliente_produto, x='Liquido Mov.', y='Nome', title='Receita Liquida por Cliente'
                        , labels={'Liquido Mov.': 'Total Movimentado', 'Nome': 'Cliente'}, orientation='h'
                        , color='Nome Artigo', height=800, width=800,
                        template='plotly_dark', hover_name='Nome', hover_data=['Liquido Mov.'], text='Liquido Mov.')

fig_cliente = fig_cliente.update_layout(yaxis_categoryorder='total ascending')
st.plotly_chart(fig_cliente, use_container_width=True)

# Faturamento por Produto/Cliente
fig_produto = px.bar(gasto_cliente_produto, x='Liquido Mov.', y='Nome Artigo', title='Receita Liquida por Produto'
                        , labels={'Liquido Mov.': 'Total Movimentado', 'Nome Artigo': 'Produto'}, orientation='h'
                        , color='Nome', height=800, width=800,
                        template='plotly_dark', hover_name='Nome Artigo', hover_data=['Liquido Mov.'], text='Liquido Mov.')

fig_produto = fig_produto.update_layout(yaxis_categoryorder='total ascending', xaxis_title='Total Movimentado')
st.plotly_chart(fig_produto, use_container_width=True)
