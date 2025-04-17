import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import datasets
import plotly.express as px

st.set_page_config(
    page_title="Análise de Datasets",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_example_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['target'] = data.target
        df['species'] = df['target'].map({
            0: 'setosa',
            1: 'versicolor',
            2: 'virginica'
        })
        return df
    elif dataset_name == "Boston Housing":
        data = datasets.fetch_california_housing()
        df = pd.DataFrame(data.data, columns=data.feature_names)
        df['PRICE'] = data.target
        return df
    return None

st.title("📊 Análise Exploratória de Dados")
st.markdown("""
Esta aplicação permite analisar datasets através de visualizações interativas e estatísticas descritivas.
* Faça upload de um arquivo CSV ou Excel
* Ou selecione um dataset de exemplo
* Explore os dados e crie diferentes visualizações
""")

st.sidebar.header("📁 Carregamento de Dados")

load_option = st.sidebar.radio(
    "Escolha como carregar os dados:",
    ["Upload de arquivo", "Dataset de exemplo"]
)

df = None

if load_option == "Upload de arquivo":
    st.sidebar.subheader("Upload de Arquivo")
    uploaded_file = st.sidebar.file_uploader("Escolha um arquivo CSV ou Excel", type=["csv", "xlsx", "xls"])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.sidebar.success(f"Arquivo '{uploaded_file.name}' carregado com sucesso!")
        except Exception as e:
            st.sidebar.error(f"Erro ao carregar o arquivo: {e}")

else:
    st.sidebar.subheader("Dataset de Exemplo")
    example_dataset = st.sidebar.selectbox(
        "Selecione um dataset de exemplo:",
        ["Iris", "Boston Housing"]
    )
    
    df = load_example_dataset(example_dataset)
    if df is not None:
        st.sidebar.success(f"Dataset '{example_dataset}' carregado com sucesso!")

if df is not None:
    st.header("🔍 Visão Geral dos Dados")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Dimensões do Dataset:**", df.shape)
    with col2:
        st.write("**Colunas:**", ", ".join(df.columns))
    
    st.subheader("Primeiras Linhas")
    num_rows = st.slider("Número de linhas para visualizar", 5, 50, 10)
    st.dataframe(df.head(num_rows))
    
    st.header("📈 Estatísticas Descritivas")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        selected_cols = st.multiselect(
            "Selecione colunas para análise estatística:",
            numeric_cols,
            default=numeric_cols[:min(3, len(numeric_cols))]
        )
        
        if selected_cols:
            st.dataframe(df[selected_cols].describe())
            
            st.subheader("Matriz de Correlação")
            corr = df[numeric_cols].corr()
            fig, ax = plt.subplots(figsize=(10, 8))
            mask = np.triu(np.ones_like(corr, dtype=bool))
            cmap = sns.diverging_palette(230, 20, as_cmap=True)
            sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0,
                        annot=True, fmt=".2f", square=True, linewidths=.5, ax=ax)
            st.pyplot(fig)

    st.header("🔍 Filtragem de Dados")
    st.write("Use os controles abaixo para filtrar o dataset:")
    
    filter_container = st.container()
    
    with filter_container:
        filter_cols = st.multiselect("Selecione colunas para filtrar:", df.columns)
        
        filtered_df = df.copy()
        
        if filter_cols:
            for col in filter_cols:
                if pd.api.types.is_numeric_dtype(df[col]):
                    min_val, max_val = float(df[col].min()), float(df[col].max())
                    step = (max_val - min_val) / 100
                    filter_val = st.slider(f"Filtrar {col}", min_val, max_val, (min_val, max_val), step=step)
                    filtered_df = filtered_df[(filtered_df[col] >= filter_val[0]) & (filtered_df[col] <= filter_val[1])]
                else:
                    unique_vals = df[col].unique().tolist()
                    selected_vals = st.multiselect(f"Filtrar {col}", unique_vals, default=unique_vals)
                    if selected_vals:
                        filtered_df = filtered_df[filtered_df[col].isin(selected_vals)]
        
        if not filtered_df.equals(df):
            st.subheader("Dados Filtrados")
            st.write(f"Mostrando {len(filtered_df)} de {len(df)} registros")
            st.dataframe(filtered_df)

    st.header("🎨 Visualizações")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Histogramas", "Scatter Plot", "Box Plot", "Gráfico 3D"])
    
    with tab1:
        st.subheader("Histograma")
        hist_col = st.selectbox("Selecione uma coluna para o histograma:", numeric_cols)
        if hist_col:
            fig = px.histogram(df, x=hist_col, nbins=30, title=f"Histograma de {hist_col}")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.subheader("Gráfico de Dispersão")
        if len(numeric_cols) >= 2:
            col_x = st.selectbox("Selecione a coluna para o eixo X:", numeric_cols, index=0)
            col_y = st.selectbox("Selecione a coluna para o eixo Y:", numeric_cols, index=min(1, len(numeric_cols)-1))
            
            color_options = ["Nenhum"] + df.columns.tolist()
            color_col = st.selectbox("Colorir por (opcional):", color_options)
            
            color_param = None if color_col == "Nenhum" else color_col
            
            fig = px.scatter(df, x=col_x, y=col_y, color=color_param, 
                            title=f"{col_y} vs {col_x}",
                            labels={col_x: col_x, col_y: col_y})
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.subheader("Box Plot")
        box_col = st.selectbox("Selecione uma coluna para o box plot:", numeric_cols)
        
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        group_options = ["Nenhum"] + categorical_cols
        group_col = st.selectbox("Agrupar por (opcional):", group_options)
        
        if box_col:
            if group_col != "Nenhum" and len(df[group_col].unique()) <= 10:  # Limita para não ter muitos grupos
                fig = px.box(df, y=box_col, x=group_col, title=f"Box Plot de {box_col} por {group_col}")
            else:
                fig = px.box(df, y=box_col, title=f"Box Plot de {box_col}")
            st.plotly_chart(fig, use_container_width=True)
            
    with tab4:
        st.subheader("Gráfico 3D")
        
        if len(numeric_cols) >= 3:
            col_x = st.selectbox("Selecione a coluna para o eixo X (3D):", numeric_cols, index=0)
            col_y = st.selectbox("Selecione a coluna para o eixo Y (3D):", numeric_cols, index=min(1, len(numeric_cols)-1))
            col_z = st.selectbox("Selecione a coluna para o eixo Z (3D):", numeric_cols, index=min(2, len(numeric_cols)-1))
            
            color_options = ["Nenhum"] + df.columns.tolist()
            color_col = st.selectbox("Colorir pontos por (opcional):", color_options)
            
            size_options = ["Tamanho fixo"] + numeric_cols
            size_col = st.selectbox("Tamanho dos pontos (opcional):", size_options)
            
            color_param = None if color_col == "Nenhum" else color_col
            size_param = None if size_col == "Tamanho fixo" else df[size_col]
            
            fig = px.scatter_3d(
                df, x=col_x, y=col_y, z=col_z,
                color=color_param,
                size=size_param,
                opacity=0.7,
                title=f"Visualização 3D: {col_x} vs {col_y} vs {col_z}",
                labels={
                    col_x: col_x,
                    col_y: col_y,
                    col_z: col_z
                }
            )
            
            fig.update_layout(
                scene=dict(
                    xaxis_title=col_x,
                    yaxis_title=col_y,
                    zaxis_title=col_z,
                    aspectmode='cube'  
                ),
                width=800,
                height=800,
                margin=dict(l=0, r=0, b=0, t=30)
            )
            
            st.plotly_chart(fig)
            
            with st.expander("💡 Dicas para interagir com o gráfico 3D"):
                st.markdown("""
                - **Rotação**: Clique e arraste para girar o gráfico
                - **Zoom**: Use o scroll do mouse ou o gesto de pinça no touchpad
                - **Pan**: Pressione Shift + clique e arraste
                - **Reset**: Clique duas vezes no gráfico
                - **Selecionar área**: Pressione Ctrl (ou Cmd) + clique e arraste para selecionar pontos
                """)
        else:
            st.warning("São necessárias pelo menos 3 colunas numéricas para criar um gráfico 3D.")
    
else:
    st.info("👆 Por favor, carregue um dataset usando as opções no menu lateral.")

st.markdown("---")
st.markdown("Desenvolvido para o processo seletivo da ESC.")