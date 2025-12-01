# Importamos paquetes que instalamos:
from bs4 import BeautifulSoup # Crea objeto que nos permite navegar or URL.
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import warnings # Para evitar adevertencias como dependencias.

warnings.filterwarnings("ignore")

### Funciones ###
def formato_numero(valor,prefijo=""):
    for unidad in ["", "mil"]: # Que recorra los numeros
        if valor < 1000:
            return f"{prefijo} {valor:.2f} {unidad}"
        valor /=1000
    return f"{prefijo} {valor:.2f} millones"       

# Titulo:
st.title("DASHBOARD DE VENTAS")#Luego en venv ejecutar:streamlit run dashboard.py

st.set_page_config(layout="wide") # Para que mantenga formato extendido de mapa y tabla 

# Datos API:
url = "https://ahcamachod.github.io/productos" #Copiamos el enlace y lo pegamos en una pestaña.

# Extraemos los datos de la API JSON de arriba:
response = requests.get(url) # Creamos variable Respuesta.
soup = BeautifulSoup(response.content, "html.parser") # Traemos la respuesta y traducimos a html.
datos = pd.read_json(soup.pre.contents[0]) # Leemos el contenido json con el objeto soup.
datos["Fecha de Compra"] = pd.to_datetime(datos["Fecha de Compra"], format="%d/%m/%Y") # Para el grafico Fact. Mensual

# Filtrando por Region y Año:
regiones_dict = {
    "Bogotá":"Andina", "Medellín":"Andina", "Calí":"Pacífica", "Pereira":"Andina", " Barranquilla":"Caribe", "Cartagena":"Caribe", 
    "Cúcuta":"Andina", "Bucaramanga":"Andina", "Riohacha":"Caribe", "Santa Marta":"Caribe", "Leticia":"Amazónica", "Pasto":"Andina", 
    "Manizales":"Andina", "Neiva":"Andina", "Villavicencio":"Orinoquía", "Armenia": "Andina", "Soacha":"Andina", "Valledupar":"Caribe", 
    "Inírida":"Amazónica"
}

# Creamos atrubuto Regiones:
datos["Región"] = datos["Lugar de Compra"].map(regiones_dict)
datos["Año"] = datos["Fecha de Compra"].dt.year

### SIDEBAR para la interaccion con la API: ###

regiones = ["Colombia", "Caribe", "Andina", "Pacífica", "Orinoquía", "Amazónica"]

st.sidebar.title("Filtro")
region = st.sidebar.selectbox("Región", regiones)
if region == "Colombia":
    datos = datos.loc[datos["Región"] != region]
else:
    datos = datos.loc[datos["Región"]==region]

# Creamos todos los años:
todos_años = st.sidebar.checkbox("Datos de todo periodo", value = True) 
if todos_años:
    datos = datos
else:
    año = st.sidebar.slider("Año", 2020, 2023) 
    datos = datos.loc[datos["Año"]==año] 

# Creamos filtro vendederos:
filtro_vendedores = st.sidebar.multiselect("Vendedores", datos.Vendedor.unique())
if filtro_vendedores:
    datos = datos[datos["Vendedor"].isin(filtro_vendedores)]         


### Creacion de Faetures: ###
fact_ciudades = datos.groupby("Lugar de Compra")[["Precio"]].sum()

fact_ciudades = datos.drop_duplicates(subset="Lugar de Compra")[["Lugar de Compra", "lat", "lon"]].merge(
    fact_ciudades,left_on="Lugar de Compra", right_index=True).sort_values("Precio", ascending=False)

facturacion_mensual = datos.set_index("Fecha de Compra").groupby(pd.Grouper(freq="ME"))["Precio"].sum().reset_index()

facturacion_mensual["Año"] = facturacion_mensual["Fecha de Compra"].dt.year
facturacion_mensual["Mes"] = facturacion_mensual["Fecha de Compra"].dt.month_name()

facturacion_cat = datos.groupby("Categoría del Producto")[["Precio"]].sum().sort_values("Precio", ascending=False)

vendedores = pd.DataFrame(datos.groupby("Vendedor")["Precio"].agg(["sum", "count"])) # Facturacion y cant. ventas por vendedor.

# Cantidad de ventas(pestaña 2)
# Por estado
ventas_estados = pd.DataFrame(datos.groupby("Lugar de Compra")['Precio'].count())
ventas_estados = datos.drop_duplicates(subset="Lugar de Compra")[["Lugar de Compra",'lat', 'lon']].merge(
    ventas_estados, left_on="Lugar de Compra", right_index=True).sort_values('Precio', ascending=False)

# Mensual
ventas_mensual = pd.DataFrame(datos.set_index('Fecha de Compra').groupby(pd.Grouper(freq='M'))['Precio'].count()).reset_index()
ventas_mensual['Año'] = ventas_mensual['Fecha de Compra'].dt.year
ventas_mensual['Mes'] = ventas_mensual['Fecha de Compra'].dt.month_name()

# Por prodcuto
ventas_categorias = pd.DataFrame(datos.groupby('Categoría del Producto')['Precio'].count().sort_values(ascending=False))


### Creacion de Graficos: ###

fig_fact = px.scatter_geo(fact_ciudades, lat="lat", lon="lon", scope="south america", size="Precio", template="seaborn",
    hover_name= "Lugar de Compra", hover_data={"lat":False, "lon":False}, title="Facturacion por Ciudad")

fig_facturacion_mensual = px.line(facturacion_mensual, x="Mes", y="Precio", markers=True, range_y=(0, facturacion_mensual.max()),
    color="Año", line_dash="Año", title="Facturacion Mensual") 

fig_facturacion_ciudades = px.bar(fact_ciudades.head(), x="Lugar de Compra", y="Precio", text_auto=True, title="Top ciudades (Facturacion)") 

fig_facturacion_cat = px.bar(facturacion_cat, text_auto=True, title="Facturacion por Categoria")

# Ventas por estado
fig_mapa_ventas = px.scatter_geo(ventas_estados, lat='lat', lon='lon',scope='south america', fitbounds='locations', 
    template='seaborn', size='Precio',hover_name="Lugar de Compra", hover_data={'lat': False, 'lon': False},title='Ventas por estado')

# Ventas Mansual
fig_ventas_mensual = px.line(ventas_mensual, x='Mes',y='Precio',markers=True,range_y=(0, ventas_mensual.max()), color='Año', 
    line_dash='Año',title='Cantidad de ventas mensual')

# Grafico barra ventas por estado:
fig_ventas_estados = px.bar(ventas_estados.head(),x="Lugar de Compra", y='Precio',text_auto=True,title='Top 5 estados')

# Grafico ventas por producto:
fig_ventas_categorias = px.bar(ventas_categorias, text_auto=True,title='Ventas por categoría')
                                                         
                        
### Updates: ###

fig_fact.update_geos(fitbounds="locations") # Para que nos muestre Colombia y no todo Sudamerica:

fig_facturacion_mensual.update_layout(yaxis_title="Facturacion")

fig_facturacion_ciudades.update_layout(yaxis_title="Facturacion")

fig_facturacion_cat.update_layout(yaxis_title="Facturacion")

fig_ventas_mensual.update_layout(yaxis_title='Cantidad de ventas')   

fig_ventas_estados.update_layout(yaxis_title='Cantidad de ventas') # Barra 

fig_ventas_categorias.update_layout(showlegend=False, yaxis_title='Cantidad de ventas')


### Agregamos Tablas para crear Pestañas: ###
tab1, tab2, tab3 = st.tabs(["Facturacion", "Cantidad de Ventas", "Vendedores"]) # Agregamos las pestañas que tendras los datos.

with tab1:
# Modificamos posicion de las metricas:
    col1, col2 = st.columns(2)
    with col1:
    # Agregamos metricas informativas:
        st.metric("Facturacion",formato_numero(datos["Precio"].sum(), "COP")) # Facturacion total
        st.plotly_chart(fig_fact, width="stretch") # Metrica de Grafico.
        st.plotly_chart(fig_facturacion_ciudades, width="stretch")
    with col2:    
        st.metric("Cantidad de ventas",formato_numero(datos.shape[0]))
        st.plotly_chart(fig_facturacion_mensual, width='stretch')
        st.plotly_chart(fig_facturacion_cat, width="stretch")

with tab2:
# Modificamos posicion de las metricas:
    col1, col2 = st.columns(2)
    with col1:
    # Agregamos metricas informativas:
        st.metric('Ingresos', formato_numero(datos['Precio'].sum(), 'COP'))
        st.plotly_chart(fig_mapa_ventas, width="stretch")
        st.plotly_chart(fig_ventas_estados, width="stretch")
        
    with col2:    
        st.metric("Cantidad de ventas",formato_numero(datos.shape[0]))
        st.plotly_chart(fig_ventas_mensual, width="stretch")
        st.plotly_chart(fig_ventas_categorias, width="stretch")

with tab3:
    ct_vendedores = st.number_input("Cantidad de vendedores", 2, 10, 5)    
# Modificamos posicion de las metricas:
    col1, col2 = st.columns(2)
    with col1:
    # Agregamos metricas informativas:
        st.metric("Facturacion",formato_numero(datos["Precio"].sum(), "COP")) # Facturacion total
        # Metrica y grafica de fact por vendedor:
        fig_facturacion_vendedores = px.bar(vendedores[["sum"]].sort_values("sum").head(ct_vendedores), x="sum", y=vendedores
        [["sum"]].sort_values("sum").head(ct_vendedores).index, text_auto=True, 
        title= f"Top {ct_vendedores} vendedores (Facturacion)")
        st.plotly_chart(fig_facturacion_vendedores)
        
    with col2:    
        st.metric("Cantidad de ventas",formato_numero(datos.shape[0]))
        # Metrica y grafica de cant de ventas por vendedor:
        fig_cantidad_ventas = px.bar(vendedores[["count"]].sort_values("count").head(ct_vendedores), x="count", y=vendedores
        [["count"]].sort_values("count").head(ct_vendedores).index, text_auto=True, 
        title= f"Top {ct_vendedores} vendedores (Cantidad de ventas)")
        st.plotly_chart(fig_cantidad_ventas)
                
            

# Representamos df en el Dashboard de Streamlit:
st.dataframe(datos) # Si no queremos ver grafico, comentamos(#)

