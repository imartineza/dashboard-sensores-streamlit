import streamlit as st
import pandas as pd
import plotly.express as px
from supabase import create_client
from streamlit_autorefresh import st_autorefresh
# =====================================
# CONFIGURACIÓN DE LA PÁGINA
# =====================================

st.set_page_config(
    page_title="Dashboard Industrial", 
    page_icon="📊",
    layout="wide"
)
st_autorefresh(interval=5000, key="dashboard")
# =====================================
# CONEXIÓN A SUPABASE
# =====================================

SUPABASE_URL = "https://cntehpvbtqzusubvkcdo.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImNudGVocHZidHF6dXN1YnZrY2RvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODM0Nzk1NzIsImV4cCI6MjA5OTA1NTU3Mn0.AE1Anmh48cHxkurc2wOhdUrbVlZVx4jGeE-FO25dnWo"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# =====================================
# CONSULTAR DATOS
# =====================================

respuesta = supabase.table(
    "tabla_dato_sensor_valores"
).select("*").execute()

df = pd.DataFrame(respuesta.data)

# =====================================
# TÍTULO
# =====================================

st.title("📊 Dashboard de Sensores Industriales")

st.write("Visualización de datos almacenados en Supabase")

st.divider()

# =====================================
# TARJETAS KPI
# =====================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Registros",
    len(df)
)

col2.metric(
    "Temperatura",
    f'{df[df.sensor=="Temperatura"]["valor"].iloc[0]} °C'
)

col3.metric(
    "Humedad",
    f'{df[df.sensor=="Humedad"]["valor"].iloc[0]} %'
)

col4.metric(
    "Presión",
    f'{df[df.sensor=="Presión"]["valor"].iloc[0]} kPa'
)

st.divider()

# =====================================
# TABLA
# =====================================

st.subheader("Datos almacenados")

st.dataframe(
    df,
    use_container_width=True
)

st.divider()

# =====================================
# GRÁFICAS
# =====================================

col1, col2 = st.columns(2)

with col1:

    grafica_barras = px.bar(
        df,
        x="sensor",
        y="valor",
        color="sensor",
        text="valor",
        title="Valor por Sensor"
    )

    st.plotly_chart(
        grafica_barras,
        use_container_width=True
    )

with col2:

    grafica_pastel = px.pie(
        df,
        names="sensor",
        values="valor",
        title="Distribución de Valores"
    )

    st.plotly_chart(
        grafica_pastel,
        use_container_width=True
    )

st.divider()

grafica_linea = px.line(
    df,
    x="fecha",
    y="valor",
    color="sensor",
    markers=True,
    title="Valores registrados"
)

st.plotly_chart(
    grafica_linea,
    use_container_width=True
)

st.success("Dashboard conectado correctamente con Supabase.")