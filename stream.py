# ---------- Librerias ----------
import pandas as pd  # instalamos pandas y openpyxl
import plotly.express as px 
import streamlit as st
from collections import Counter

# ---------- Configuracion inicial de la pagina ----------
#Pagina para obtener emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title='Sales Ecommerce Dashboard',
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

years = st.sidebar.multiselect(
    label='Selecciona el Año:',
    options=df['Year'].unique(),
    default=df['Year'].unique(),
    disabled=False
)
st.sidebar.write(years)

months = st.sidebar.slider(
    label='Selecciona el Mes',
    min_value=1,
    max_value=12
)
# st.sidebar.write(months)

days = st.sidebar.slider(
    label='Selecciona el Día',
    min_value=1,
    max_value=31
)
# st.sidebar.write(days)

hours = st.sidebar.slider(
    label='Selecciona la Hora',
    min_value=6,
    max_value=20
)
# st.sidebar.write(hours)

# ---------- Mainpage ----------
st.title('Ventas E-Commerce Dashboard')

# ---------- Metricas ----------

#Ventas Totales
total_sales = round(df['TotalSale'].sum(),2)

#Venta promedio por venta
mean_sale = round(df['TotalSale'].mean(),2)

#Producto mas vendido
counting_sold_products = Counter(df['Description'])
most_sold_products = counting_sold_products.most_common()
top_product = most_sold_products[0][0]

# ---------- Division en 3 columnas ----------

left_column, middle_column, right_column, right_right_column = st.columns(4)
with left_column:
    st.subheader('Total Ventas')
    st.subheader('US $ {}'.format(total_sales))

with middle_column:
    st.subheader('Venta Promedio Por Venta')
    st.subheader('US $ {}'.format(mean_sale))

with right_column:
    st.subheader('Producto Mas Vendido')
    st.subheader('{}'.format(top_product))

with right_right_column:
    st.subheader('Producto Con Mas Ventas')
    st.subheader('{}'.format(top_product))

st.markdown("""---""")

#  ---------- Creando dataframe editable en tiempo real ----------

df_editable = df.query('Hour == @hours & Day == @days & Month == @months')

#  ---------- Graficas  ----------

#  ---------- Ventas por Hora  ---------- 
ventas_por_hora = df_editable.groupby(by=['Hour']).sum()[['TotalSale']]
fig_ventas_por_hora = px.bar(
    ventas_por_hora,
    x=ventas_por_hora.index,
    y='TotalSale',
    title='<b>Ventas por Hora</b>',
    color='TotalSale'
)
fig_ventas_por_hora.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=True)),
)

#  ---------- Ventas por Dia  ---------- 
ventas_por_dia = df_editable.groupby(by=['Day']).sum()[['TotalSale']]
fig_ventas_por_dia = px.bar(
    ventas_por_dia,
    x=ventas_por_dia.index,
    y='TotalSale',
    title='<b>Ventas por Dia</b>',
    color='TotalSale'
)
fig_ventas_por_dia.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor='rgba(0,0,0,0)',
    yaxis=(dict(showgrid=True)),
)

left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_ventas_por_hora, use_container_width=True)
right_column.plotly_chart(fig_ventas_por_dia, use_container_width=True)

st.markdown("""---""")

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

# ---- Ocultar barra de carga streamlit----

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """

st.markdown(hide_st_style, unsafe_allow_html=True)