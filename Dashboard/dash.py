import pandas as pd
import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt
from typing import List, Tuple

def set_page_config():
    st.set_page_config(
        page_title="Dashboard Câncer",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown("<style> footer {visibility: hidden;} </style>", unsafe_allow_html=True)

set_page_config()

@st.cache_data
def load_data():
    df = pd.read_parquet('../data/parquet/dataSetFinalTratado.parquet')
    df['Data de Diagnostico'] = pd.to_datetime(df['Data de Diagnostico'], format='%d/%m/%Y')

    return df

@st.cache_data
def load_data_disease():
    df = pd.read_parquet('../data/parquet/dataSetFinalTratadoTop5Diseases.parquet')
    df['Data de Diagnostico'] = pd.to_datetime(df['Data de Diagnostico'], format='%d/%m/%Y')

    return df

def load_line_chart(data):
    plt.rcParams['agg.path.chunksize'] = 10000

    st.subheader("Casos Totais de Câncer")
    data = data.sort_values(by='Data de Diagnostico')
    data = data.set_index('Data de Diagnostico')

    result = data.resample("M")['Nome do RCBP'].count()

    st.line_chart(result)

def load_line_chart_by_region(region, data):
    df_filtered = data[data['Regiao'] == region]

    plt.rcParams['agg.path.chunksize'] = 10000

    st.subheader("Casos Totais de Câncer Filtrado por Região")
    df_filtered = df_filtered.sort_values(by='Data de Diagnostico')
    df_filtered = df_filtered.set_index('Data de Diagnostico')

    result = df_filtered.resample("M")['Nome do RCBP'].count()

    st.line_chart(result)

def load_line_chart_by_rcbp(rcbp, data):
    df_filtered = data[data['Nome do RCBP'] == rcbp]

    plt.rcParams['agg.path.chunksize'] = 10000

    st.subheader("Casos Totais de Câncer Filtrado por RCBP")
    df_filtered = df_filtered.sort_values(by='Data de Diagnostico')
    df_filtered = df_filtered.set_index('Data de Diagnostico')

    result = df_filtered.resample("M")['Nome do RCBP'].count()

    st.line_chart(result)

def load_status_vital_by_region_bar_chart(data):
    st.subheader("Distribuição de Status Vital por Região")
    grouped = data.groupby(['Status Vital', 'Regiao']).size().unstack(fill_value=0)
    grouped['Total'] = grouped.sum(axis=1)
    grouped = grouped.T

    st.bar_chart(grouped, height=1000)

def load_top_diseases_by_region(data):
    grouped_df = data.groupby(['Regiao', 'categoria_doenca']).size().reset_index(name='counts')

    fig = px.bar(grouped_df, x='Regiao', y='counts', color='categoria_doenca', 
                 labels={'Regiao': 'Região', 'counts': 'Número de Casos', 'categoria_doenca': 'Tipo de Câncer'},
                 text='counts')  # Adiciona os rótulos de texto

    # Ajuste o layout para garantir que os labels fiquem na parte inferior
    fig.update_layout(
        xaxis=dict(title='Região', title_standoff=25),
        yaxis=dict(title='Número de Casos'),
        legend=dict(orientation='h', yanchor='bottom', y=-0.3, xanchor='center', x=0.5)
    )

    # Atualiza a posição dos rótulos de texto para estar sempre visível e ajustado
    fig.update_traces(texttemplate='%{text}', textposition='outside')

    st.subheader('Distribuição de Tipos de Câncer por Região no Brasil')
    st.plotly_chart(fig, use_container_width=True)  # Use container_width para ajustar automaticamente

# main program =================================================================================>

# df = load_data()
df = load_data_disease()

st.title("Dashboard de Análise de Câncer")

load_line_chart(df)

selected_region = st.selectbox("Selecione a Região", options=df['Regiao'].unique(), index=0)
load_line_chart_by_region(selected_region, df)

selected_rcbp = st.selectbox("Selecione o RCBP", options=df['Nome do RCBP'].unique(), index=0)
load_line_chart_by_rcbp(selected_rcbp, df)

load_status_vital_by_region_bar_chart(df)

load_top_diseases_by_region(df)