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

# Datos API:
url = "https://ahcamachod.github.io/productos" #Copiamos el enlace y lo pegamos en una pestaña.

# Extraemos los datos de la API JSON de arriba:
response = requests.get(url) # Creamos variable Respuesta.
soup = BeautifulSoup(response.content, "html.parser") # Traemos la respuesta y traducimos a html.
datos = pd.read_json(soup.pre.contents[0]) # Leemos el contenido json con el objeto soup.

# Modificamos posicion de las metricas:
col1, col2 = st.columns(2)

with col1:
# Agregamos metricas informativas:
    st.metric("Facturacion",formato_numero(datos["Precio"].sum(), "COP")) # Facturacion total
with col2:    
    st.metric("Cantidad de ventas",formato_numero(datos.shape[0]))

# Representamos df en el Dashboard de Streamlit:
st.dataframe(datos)

