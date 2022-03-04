# ---------- Librerias ----------

import pandas as pd
import plotly.express as px
import streamlit as st

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
st.sidebar.header('Selecciona la fecha')

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
most_product = df['Description'].value_counts()
top_sale = most_product.index[0]

#Producto con mas ventas
top = df.groupby('Description').agg(sum)[['TotalSale']]
top_product = top.index[0]

# ---------- Division en 3 columnas ----------

metric_1, metric_2, metric_3, metric_4 = st.columns(4)
with metric_1:
    st.subheader('Total Ventas')
    st.caption('US $ {}'.format(total_sales))

with metric_2:
    st.subheader('Venta Promedio Por Venta')
    st.caption('US $ {}'.format(mean_sale))

with metric_3:
    st.subheader('Producto Mas Vendido')
    st.caption('{}'.format(top_sale))

with metric_4:
    st.subheader('Producto Con Mas Ventas')
    st.caption('{}'.format(top_product))

st.markdown("""---""")

#  ---------- Creando dataframe editable en tiempo real ----------

df_editable = df.query('Hour == @hours & Day == @days')

#  ---------- Graficas  ----------

#  ---------- Ventas por Mes  ----------
meses = {
    1:'Enero',
    2:'Febrero',
    3:'Marzo',
    4:'Abril',
    5:'Mayo',
    6:'Junio',
    7:'Julio',
    8:'Agosto',
    9:'Septiembre',
    10:'Octubre',
    11:'Noviembre',
    12:'Diciembre'
}

ventas_por_mes = df_editable.groupby(by=['Month']).sum()[['TotalSale']]
fig_ventas_por_mes = px.bar(
    ventas_por_mes,
    x=ventas_por_mes.index.map(meses),
    y='TotalSale',
    title='<b>Ventas por Mes</b>',
    color_discrete_sequence=px.colors.sequential.Reds
)
fig_ventas_por_mes.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=True))
)

#  ---------- Ventas Totales en Porcentajes ----------

fig = px.pie(df_editable,
    values='TotalSale',
    names=df_editable.Month.map(meses),
    color_discrete_sequence=px.colors.sequential.Reds,
    title='<b>Ventas Totales</b>'
)

fig.update_layout(
    xaxis=dict(tickmode='linear'),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=True))
)

column_1, column_2 = st.columns(2)
column_1.plotly_chart(fig_ventas_por_mes, use_container_width=True)
column_2.plotly_chart(fig, use_container_width=True)

#  ---------- Charts  ----------

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
    df = df.drop(['Year'],axis=1)
    df['Month'] = df['Month'].map(meses)
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df(df_editable)

# ---- Boton de Descarga ----
st.sidebar.header('Descargar Dataframe')

st.sidebar.download_button(
    label="Descarga CSV",
    data=csv,
    file_name='ventas2011.csv',
    mime='text/csv',
)
