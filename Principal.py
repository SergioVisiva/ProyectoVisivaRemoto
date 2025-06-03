import streamlit as st
import pandas as pd
import sqlitecloud
import Pipeline as pv 

# Conexión a la BD SQLite Cloud
con_sql = sqlitecloud.connect(
    "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
)

st.sidebar.header("Navegación")

# Opciones del menú con emojis
opciones = ["📋 Pipeline", "📈 Base Gestionable", "🗂️ Bases HSM"]

# Selector tipo radio para que siempre se vean las opciones y se mantenga el estado
pagina = st.sidebar.radio("Selecciona la página:", opciones)

# Guardar la selección en session_state
st.session_state.pagina = pagina


if pagina == "📋 Pipeline":
    pv.obtener_datos_filtrados_por_equipo(con_sql, pagina)


con_sql.close()


