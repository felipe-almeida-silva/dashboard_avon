import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# config page
st.set_page_config(
    page_title="Dashboard VBHC Avon",
    layout="wide",
    initial_sidebar_state="auto",
)

#### loading data ####
with st.spinner('Wait for it...'):
    sheet_id = '1_oaENRMneBPwkH4-ZCPq0bFiOUuJC9UWTSkNsnBBX0g'
    xls = pd.ExcelFile(f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx')
    sheets = xls.sheet_names
    #### create DataFrame ####
    df_avon= pd.read_excel(xls, sheets[1])

# get avon logo from url
avon_logo = 'https://i.pinimg.com/originals/02/ed/30/02ed3038ba6235975923501f864519ce.png'

#### renaming columns ####
# columns name to lower case and replace space with underscore
df_avon.columns = df_avon.columns.str.lower().str.replace(' ', '_')

# get list of unique values of column nome_unidade
unidades = df_avon['nome_unidade'].unique()
unidades = np.insert(unidades, 0, 'Todas')
# unidades = unidades.insert(0, 'Todas')
print(unidades)

option = st.sidebar.selectbox('Selecione a unidade', unidades, index=0)

# filter df_avon by option else show all from unidades
if option == 'Todas':
    df_avon = df_avon.query('nome_unidade in @unidades')
else:
    df_avon = df_avon.query('nome_unidade == @option')

# filter df_avon by option
# df_avon = df_avon.query('nome_unidade in @unidades')

#### transforming data ####
# convert data_de_nascimento to datetime
df_avon['data_de_nascimento'] = pd.to_datetime(df_avon['data_de_nascimento'], format='%d/%m/%Y')

# convet data_ficha_clinica to datetime
df_avon['data_ficha_clinica'] = pd.to_datetime(df_avon['data_ficha_clinica'], format='%d/%m/%Y')

# create column age as integer from ficha clinica
df_avon['idade'] = (df_avon['data_ficha_clinica'] - df_avon['data_de_nascimento']).astype('<m8[Y]')

# create a column in df_avon with age range of 10 years interval from 0 to 100
df_avon['idade_range'] = pd.cut(df_avon['idade'], bins=[0,10,20,30,40,50,60,70,80,90,100], labels=['0-10','10-20','20-30','30-40','40-50','50-60','60-70','70-80','80-90','90-100'])

#### dataframe with unique values for colab ####
# create dataframe with unique values of codigo_funcionario
df_avon_unique_colab = df_avon.drop_duplicates(subset=['codigo_funcionario'])


#### functions ####

# create a function that receives df_avon_unique_colab and return a dataframe with the parameters and the number of unique values
def create_df_unique_values(df, col):
    df_unique_values = df.groupby([col]).count()['codigo_funcionario'].reset_index()
    df_unique_values.columns = [col,'quantidade']
    # sort values by quantidadeq
    df_unique_values = df_unique_values.sort_values(by='quantidade', ascending=False)
    return df_unique_values

# create a function to create a bar chart from a dataframe using plotly graph objects
def create_bar_chart_go(df, x, x_title, y, y_title, title, color):
    fig = go.Figure(go.Bar(x=df[x], y=df[y], marker_color=color, text=df[y]))
    fig.update_layout(title_text=title, height=600, width=1000)
    fig.update_xaxes(visible=True, showticklabels=False)
    # xaxes title  
    fig.update_xaxes(title_text=x_title)
    #yaxes title
    fig.update_yaxes(title_text=y_title)
    return fig


# create a function to create a bar chart from a dataframe
def create_bar_chart(df, x, x_title, y, y_title, title, color):
    fig = px.bar(df, x=x, y=y, color=color, text=y)
    fig.update_layout(title_text=title, height=600, width=1000)
    fig.update_xaxes(visible=True, showticklabels=False)
    # xaxes title  
    fig.update_xaxes(title_text=x_title)
    #yaxes title
    fig.update_yaxes(title_text=y_title)
    return fig

# create a function to create a pie chart from a dataframe
def create_pie_chart(df, labels, values, colors):
    fig = go.Figure(go.Pie(labels=labels, values=values, pull=[0.02],
                     textinfo='label+percent', marker_colors=colors, direction = 'clockwise',
                     insidetextorientation='radial')
    )
    return fig

# create a function to create a dataframe for plotly treemap
def create_df_treemap(df, col):
    df_treemap = df[col].value_counts().reset_index()
    df_treemap.columns = [col,'quantidade']
    # sort values by quantidade
    df_treemap = df_treemap.sort_values(by='quantidade', ascending=False)
    return df_treemap

# create a funciton to create a treemap
def create_treemap(df, col, title):
    fig = px.treemap(df, path=col, values='quantidade', color='quantidade', color_discrete_map=color_scale)
    fig.update_layout(title_text=title, height=600, width=1000)
    return fig

# create a function to create a dataframe grouped by col1 and col2
def create_df_grouped(df, col1, col2):
    df_grouped = df.groupby([col1, col2]).count()['codigo_funcionario'].reset_index()
    df_grouped.columns = [col1, col2, 'quantidade']
    # sort values by quantidade
    df_grouped = df_grouped.sort_values(by='idade_range', ascending=True)
    return df_grouped

# create a function to create a bar chart grouped by col1 and col2
def create_bar_chart_grouped(df, col1, col2, x_title, y_title, title, color_map):
    fig = px.bar(df, x=col1, y='quantidade', color=col2, barmode='group', text='quantidade', color_discrete_map=color_map)
    fig.update_layout(title_text=title, height=600, width=1000)
    # fig.update_xaxes(visible=True, showticklabels=False)
    # xaxes title  
    fig.update_xaxes(title_text=x_title)
    #yaxes title
    fig.update_yaxes(title_text=y_title)
    return fig


# create a plotly subplots with 2 charts (bar from cid_80 and pie from cid_80_top_5)
def create_subplots(df, x, x_title, y, y_title, title, color, labels, values):
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'xy'}]])
    fig.add_trace(go.Pie(labels=labels, values=values, pull=[0.02],
                     textinfo='label+percent', marker_colors=color, direction = 'clockwise'), 1, 1)
    fig.add_trace(go.Bar(x=x, y=y, marker_color=color, text=y), 1, 2)
    fig.update_layout(title_text=title, height=600, width=1000)
    fig.update_xaxes(visible=True, showticklabels=False)
    # xaxes title  
    fig.update_xaxes(title_text=x_title)
    #yaxes title
    fig.update_yaxes(title_text=y_title)
    return fig

# create a discrete color scale with 10 colors
def create_color_scale():
    color_scale = px.colors.qualitative.Plotly
    return color_scale

# create a funciton based from line 295 to 309 to create a markdown for each column using st.markdown showing unidade setores and colaboradores from df_unidades_setores_colab
def create_markdown_unidades(df_unidades_setores_colab, color_scale):
    numero_de_colunas = range(len(df_unidades_setores_colab))
    numero_de_colunas_total = numero_de_colunas[-1]+1

    if numero_de_colunas_total == 1:
        st.markdown(f'<center><font size="3" color="{color_scale[0]}">{df_unidades_setores_colab["unidade"].unique()[0]}<br>Quantidade de Setores: {df_unidades_setores_colab["setores"].unique()[0]} <br> Quantidade de Colaboradores: {df_unidades_setores_colab["colaboradores"].unique()[0]}</font></center>', unsafe_allow_html=True)

    for i in numero_de_colunas:
        j = i+1 # j is the number of columns
        if j % 3 == 0: # if j is divisible by 3
            columns = st.columns(j) # create j columns
            for k, column in enumerate(columns):
                column.markdown(f'<center><font size="3" color="{color_scale[k]}">{df_unidades_setores_colab["unidade"].unique()[k]}<br>Quantidade de Setores: {df_unidades_setores_colab["setores"].unique()[k]} <br> Quantidade de Colaboradores: {df_unidades_setores_colab["colaboradores"].unique()[k]}</font></center>', unsafe_allow_html=True)
            st.markdown('<br>', unsafe_allow_html=True)
            columns = st.columns(numero_de_colunas_total-j) # create the rest of columns
            for k, column in enumerate(columns):
                column.markdown(f'<center><font size="3" color="{color_scale[k+3]}">{df_unidades_setores_colab["unidade"].unique()[k+3]}<br>Quantidade de Setores: {df_unidades_setores_colab["setores"].unique()[k+3]} <br> Quantidade de Colaboradores: {df_unidades_setores_colab["colaboradores"].unique()[k+3]}</font></center>', unsafe_allow_html=True)


#### color scale ####
color_scale = create_color_scale()

#### prepating data for charts ####
# count of collab from df_avon_unique_colab
avon_unique_colab_count = df_avon_unique_colab['codigo_funcionario'].count()

# sexo
df_sexo = create_df_unique_values(df_avon_unique_colab, 'sexo')
fig_sexo_pie = create_pie_chart(df_sexo, df_sexo['sexo'], df_sexo['quantidade'], [color_scale[6],color_scale[5]])
fig_sexo = create_bar_chart_go(df_sexo, 'sexo', 'Sexo', 'quantidade', 'Quantidade', None, [color_scale[6],color_scale[5]])

# idade
df_idade = create_df_unique_values(df_avon_unique_colab, 'idade_range')
# sort values by idade_range
df_idade = df_idade.sort_values(by='idade_range', ascending=True)
fig_idade = create_bar_chart_go(df_idade, 'idade_range', 'Idade', 'quantidade', 'Quantidade', None, color_scale[2])
fig_idade.update_xaxes(showticklabels=True)

# create a dataframe with sexo and idade_range grouped using create_df_grouped
df_sexo_idade = create_df_grouped(df_avon_unique_colab, 'sexo','idade_range')
# create a figure plotly bar chart from dataframe df_sexo_idade using create_bar_chart_grouped
fig_sexo_idade = create_bar_chart_grouped(df_sexo_idade, 'idade_range', 'sexo', 'quantidade', 'Quantidade', None, {'Feminino':color_scale[6],'Masculino':color_scale[5]})


# create a list with all nome_unidade
unidades = df_avon_unique_colab['nome_unidade'].unique().tolist()
# a dict with key = nome_unidade and value = unique count of nome_setor
unidades_setores = {}
for unidade in unidades:
    unidades_setores[unidade] = df_avon_unique_colab[df_avon_unique_colab['nome_unidade'] == unidade]['nome_setor'].nunique()

# a dict with key = nome_unidade and value = count of codigo_funcionario
unidades_colab = {}
for unidade in unidades:
    unidades_colab[unidade] = df_avon_unique_colab[df_avon_unique_colab['nome_unidade'] == unidade]['codigo_funcionario'].count()

# create a dataframe with unidades_setores and unidades_colab
df_unidades_setores_colab = pd.DataFrame(list(unidades_setores.items()), columns=['unidade','setores'])
df_unidades_setores_colab['colaboradores'] = df_unidades_setores_colab['unidade'].map(unidades_colab)
# sort values by colaboradores
df_unidades_setores_colab = df_unidades_setores_colab.sort_values(by='colaboradores', ascending=False)


# unidades
df_unidades = create_df_unique_values(df_avon_unique_colab, 'nome_unidade')
fig_unidades = create_bar_chart_go(df_unidades, 'nome_unidade', 'Unidades', 'quantidade', 'Quantidade', None, color_scale)
fig_unidades.update_xaxes(showticklabels=True, tickangle=-45)

# create figure icicle from df_avon_unique_colab
df_treemap = df_avon_unique_colab[['nome_unidade','nome_setor','nome_cargo']].value_counts().reset_index()
df_treemap.columns = ['unidade','setor','cargo','quantidade']
# create figure plotly icicle chart from dataframe df_icicle
fig_treemap = px.treemap(df_treemap, path=['unidade','setor','cargo'], 
                            values='quantidade', title='',
                            color='unidade',
                            color_discrete_map={'AVON COSMETICOS - CABREUVA':color_scale[0],
                                                'AVON INDUSTRIAL - INTERLAGOS - MATRIZ':color_scale[1],
                                                'AVON COSMETICOS - SIMÕES FILHO - BA':color_scale[2],
                                                'AVON COSMETICOS - MATRIZ':color_scale[3],
                                                'AVON COSMETICOS - NASP':color_scale[4],})


## CID
# create a dataframe with the count of cid grouped by cid from df_avon using cid column
df_cid = df_avon['cid'].value_counts().reset_index()
df_cid.columns = ['cid','quantidade']
df_cid.index = range(1, df_cid.shape[0] + 1)
# print(df_cid)
# get the top 10 cid
df_cid_top_10 = df_cid.head(10)


# create a figure plotly bar chart from dataframe df_cid using create_bar_chart_go
fig_cid = create_bar_chart_go(df_cid_top_10, 'cid', 'CID', 'quantidade', 'Quantidade', None, color_scale)
fig_cid.update_xaxes(showticklabels=True)

# create a Figure plotly pie chart from dataframe df_cid using create_pie_chart_go
fig_cid_pie = create_pie_chart(df_cid_top_10, df_cid_top_10['cid'], df_cid_top_10['quantidade'], color_scale)

# create a dataframe with the count of cid grouped by sexo from df_avon using cid column
df_cid_sexo = df_avon.groupby(['cid','sexo'])['codigo_funcionario'].count().reset_index()
df_cid_sexo.columns = ['cid','sexo','quantidade']
# sort values by quantidade and get top 10 cid
df_cid_sexo_top_10 = df_cid_sexo.query('cid in @df_cid_top_10.cid').sort_values(by='quantidade', ascending=False)
# create a figure plotly bar chart from dataframe df_cid_sexo using create_bar_chart_grouped
fig_cid_sexo = create_bar_chart_grouped(df_cid_sexo_top_10, 'cid', 'sexo', 'quantidade', 'Quantidade', None, {'Feminino':color_scale[6],'Masculino':color_scale[5]})
fig_cid_sexo.update_xaxes(showticklabels=True)

# create a dataframe with the count of cid grouped by idade_range from df_avon using cid column
df_cid_idade = df_avon.groupby(['cid','idade_range'])['codigo_funcionario'].count().reset_index()
df_cid_idade.columns = ['cid','idade_range','quantidade']
df_cid_idade = df_cid_idade.query('quantidade > 0')
# sort values by idade_range
df_cid_idade = df_cid_idade.sort_values(by='idade_range', ascending=True)

# create a figure plotly bar chart from dataframe df_cid_idade using create_bar_chart_grouped
fig_cid_idade = create_bar_chart_grouped(df_cid_idade, 'idade_range', 'cid', 'quantidade', 'Quantidade', None, {'0-20':color_scale[0],'21-30':color_scale[1],'31-40':color_scale[2],'41-50':color_scale[3],'51-60':color_scale[4],'61-70':color_scale[5],'71-80':color_scale[6],'81-90':color_scale[7],'91-100':color_scale[8]})
fig_cid_idade.update_xaxes(showticklabels=True)



### charts ###
# create a dashboard with charts and tables using streamlit from the figures created above
st.title('Dashboard Avon')
st.markdown('Dashboard criado para analisar os dados da Avon')

# create 2 columns using st.columns one for logo and other for avon_unique_colab_count
col1, col2, col3 = st.columns(3)
# create a logo using st.image
col1.image(avon_logo, width=400, use_column_width=True)

# style for centering metric label and value
st.markdown('''
<style>
/*center metric label*/
[data-testid="stMetricLabel"] > div:nth-child(1) {
    justify-content: center;
}

/*center metric value*/
[data-testid="stMetricValue"] > div:nth-child(1) {
    justify-content: center;
}
</style>
''', unsafe_allow_html=True)

# create a metric using st.metric for avon_unique_colab_count
col2.metric('Colaboradores', avon_unique_colab_count)
# create a metric using st.metric for datetime.now
col3.metric('HOJE', datetime.now().strftime('%d/%m/%Y'))

# create 2 columns using st.columns for fig_sexo and fig_sexo_pie
st.markdown('## Sexo')
col1, col2 = st.columns(2)
# create a bar chart using st.plotly_chart for fig_sexo
col1.plotly_chart(fig_sexo, use_container_width=True)
# create a pie chart using st.plotly_chart for fig_sexo_pie
col2.plotly_chart(fig_sexo_pie, use_container_width=True)

# create 2 columns using st.columns for fig_idade and fig_sexo_idade
st.markdown('## Idade')
col1, col2 = st.columns(2)
# create a bar chart using st.plotly_chart for fig_idade
col1.plotly_chart(fig_idade, use_container_width=True)
# create a bar chart using st.plotly_chart for fig_sexo_idade
col2.plotly_chart(fig_sexo_idade, use_container_width=True)


# create 2 columns using st.columns for fig_unidades and fig_treemap
st.markdown('## Unidades')
create_markdown_unidades(df_unidades_setores_colab, color_scale)


col6, col7 = st.columns(2)
# create a bar chart using st.plotly_chart for fig_unidades
col6.plotly_chart(fig_unidades, use_container_width=True)
# create a treemap using st.plotly_chart for fig_treemap
col7.plotly_chart(fig_treemap, use_container_width=True)


st.markdown('## CID')
st.dataframe(df_cid.T)
# create 2 columns using st.columns for fig_cid and fig_cid_pie
col1, col2 = st.columns(2)
col1.plotly_chart(fig_cid, use_container_width=True)
col2.plotly_chart(fig_cid_pie, use_container_width=True)

# create 2 columns using st.columns for fig_cid_sexo and fig_cid_idade
st.markdown('## CID por Sexo e Idade')
st.plotly_chart(fig_cid_sexo, use_container_width=True)
st.plotly_chart(fig_cid_idade, use_container_width=True)
