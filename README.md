# dashboard-ventas-streamlit
Repositorio que contiene el deshboard de ventas de una empresa utilizando STREAMLIT

# 📊 DASHBOARD DE VENTAS: Web Scraping y Visualización con Streamlit

[![Python](https://img.shields.io/badge/Python-3670A0?style=flat&logo=python&logoColor=ffdd54)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-2391C5?style=flat&logo=plotly&logoColor=white)](https://plotly.com/python/)
[![Requests](https://img.shields.io/badge/Requests-000000?style=flat&logo=python&logoColor=white)](https://docs.python-requests.org/en/latest/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-000000?style=flat&logo=python&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

Este proyecto implementa un **Dashboard Interactivo de Ventas** desarrollado en Python utilizando **Streamlit**. Su propósito es demostrar una solución completa de inteligencia de negocios (BI) que incluye la adquisición de datos mediante técnicas de *web scraping* (o consumo de API), su procesamiento y una visualización dinámica y organizada con gráficos interactivos.

---

## 🎯 Objetivos del Proyecto

1.  **Adquisición de Datos:** Extraer datos de ventas de una fuente externa (API/URL) mediante `requests` y `BeautifulSoup`.
2.  **Procesamiento y Transformación:** Limpiar y estructurar los datos con **Pandas**.
3.  **Visualización Interactiva:** Crear un dashboard web dinámico con métricas (KPIs), filtros y gráficos interactivos utilizando **Streamlit** y **Plotly Express**.
4.  **Análisis de Desempeño:** Mostrar métricas clave de facturación, cantidad de ventas y desempeño por vendedor y categoría.

---

## 🧠 Metodología y Componentes Clave

### 1. Extracción de Datos (Web Scraping / API Fetching)

El script se conecta a una URL específica (`https://ahcamachod.github.io/productos`) para obtener un conjunto de datos en formato JSON incrustado en una página HTML.

* Se utiliza **`requests`** para realizar la solicitud HTTP.
* **`BeautifulSoup`** se emplea para analizar el contenido HTML y localizar y extraer el *string* JSON crudo, el cual es luego leído por **Pandas**.

### 2. Preparación y Limpieza de Datos

Una vez extraídos, los datos se cargan en un *DataFrame* de Pandas, donde se realizan transformaciones esenciales:

* **Conversión de Tipo:** Se convierte la columna `"Fecha de Compra"` a tipo `datetime` para permitir el análisis temporal.
* **Función de Formato:** Se define la función `formato_numero` para presentar las métricas financieras y de conteo de manera legible (e.g., "1.50 mil", "2.30 millones").

### 3. Interfaz y Visualización con Streamlit

El dashboard se estructura de manera organizada y modular:

* **Configuración:** Se establece el diseño de la página en formato amplio (`st.set_page_config(layout="wide")`).
* **Pestañas (`st.tabs`):** El contenido se organiza en pestañas lógicas (implícitamente para Resumen, Gráficas Detalladas, Vendedores, etc., según la estructura `with tabX:`).
* **Métricas Clave (KPIs):** Se utiliza `st.metric` para mostrar indicadores importantes como la facturación total y la cantidad de ventas.

### 4. Análisis Gráfico con Plotly

Se utiliza **Plotly Express** para generar visualizaciones interactivas de alto impacto:

* **Tendencia Mensual:** Gráfico que muestra la evolución de las ventas a lo largo del tiempo.
* **Distribución por Categoría:** Gráfico que muestra la distribución de las ventas entre las diferentes categorías de productos.
* **Análisis de Vendedores:** Gráficos de barra que presentan el **Top N** de vendedores por facturación y por cantidad de ventas, donde `N` es configurable por el usuario mediante un *widget* `st.number_input`.

---


