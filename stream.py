# ---------- Librerias ----------

from operator import index
from pickle import TRUE
import pandas as pd  # instalamos pandas y openpyxl
import plotly.express as px 
import streamlit as st
from collections import Counter

# ---------- Configuracion inicial de la pagina ----------
#Pagina para obtener emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Dashboard Ventas E-commerce',
                    page_icon=':bar_chart:',
                    layout='wide'
                    )

# ---------- Abrimos y leemos el archivo ----------
@st.cache
def get_data_from_excel():
    df = pd.read_csv(
        'C:/Users/Hugo Pérez/Desktop/env/data/data_clean.csv'
        )
    return df

df = get_data_from_excel()

# ---------- Sidebar ----------
st.sidebar.header('Filtrar Información')

# years = st.sidebar.multiselect(
#     label='Selecciona el Año:',
#     options=df['Year'].unique(),
#     default=df['Year'].unique(),
#     disabled=False
# )
# st.sidebar.write(years)

# months = st.sidebar.slider(
#     label='Selecciona el Mes',
#     min_value=1,
#     max_value=12
# )
# st.sidebar.write(months)

days = st.sidebar.slider(
    label='Selecciona el Día',
    min_value=1,
    max_value=31
)
# st.sidebar.write(days)

hours = st.sidebar.slider(
    label='Selecciona la Hora',
    min_value=7,
    max_value=20
)
# st.sidebar.write(hours)

# ---------- Mainpage ----------
st.title('Dashboard Ventas E-commerce')

# ---------- Metricas ----------

#Ventas Totales
total_sales = round(df['TotalSale'].sum(),3)

#Venta promedio por venta
mean_sale = round(df['TotalSale'].mean(),3)

#Producto mas vendido
counting_sold_products = Counter(df['Description'])
most_sold_products = counting_sold_products.most_common()
top_product = most_sold_products[0][0]

top = df.groupby('Description').agg(sum)[['TotalSale']]
top_one = top.index[0] 

# ---------- Division en 3 columnas ----------

left_column, middle_column, right_column, right_right_column = st.columns(4)
with left_column:
    st.subheader('Total Ventas')
    st.caption('US $ {}'.format(total_sales))

with middle_column:
    st.subheader('Venta Promedio Por Venta')
    st.caption('US $ {}'.format(mean_sale))

with right_column:
    st.subheader('Producto Mas Vendido')
    st.caption('{}'.format(top_product))

with right_right_column:
    st.subheader('Producto Con Mas Ventas')
    st.caption('{}'.format(top_one))

st.markdown("""---""")

#  ---------- Creando dataframe editable en tiempo real ----------

df_editable = df.query('Hour == @hours & Day == @days')

#  ---------- Graficas  ----------

#  ---------- Ventas por Mes  ---------- 
ventas_por_mes = df_editable.groupby(by=['Month']).sum()[['TotalSale']]
fig_ventas_por_mes = px.bar(
    ventas_por_mes,
    x=ventas_por_mes.index,
    y='TotalSale',
    title='<b>Ventas por Mes</b>',
    color='TotalSale'
)
fig_ventas_por_mes.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=True)),
)

#  ---------- Ventas por Año  ---------- 
ventas_por_ano = df_editable.groupby(by=['Year']).sum()[['TotalSale']]
fig_ventas_por_ano = px.bar(
    ventas_por_ano,
    x=ventas_por_ano.index,
    y='TotalSale',
    title='<b>Ventas por Año</b>',
    color='TotalSale'
)
fig_ventas_por_ano.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=True)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_ventas_por_mes, use_container_width=True)
right_column.plotly_chart(fig_ventas_por_ano, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader('Top 5 Productos Mas Vendidos')
    st.dataframe(df_editable.set_index('Description')
                .sort_values(by=['TotalSale'],ascending=False)
                .drop(['Year','Month','Day','Hour'],axis=1).head()
                )

with col2:
    st.subheader('Top 5 Productos Menos Vendidos')
    st.dataframe(df_editable.set_index('Description')
                .sort_values(by=['TotalSale'],ascending=True)
                .drop(['Year','Month','Day','Hour'],axis=1).head()
                )



# ---- Ocultar barra de carga streamlit----

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)

# ---- Descargar archivo en CSV ----
@st.cache
def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_editable)

st.sidebar.header('Descargar Dataframe')

st.sidebar.download_button(
    label="Descarga CSV",
    data=csv,
    file_name='new_dataframe.csv',
    mime='text/csv',
)
