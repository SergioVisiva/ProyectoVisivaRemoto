import streamlit as st
import sqlitecloud

# raliazamos alguna configuracion de la interfas de la app
st.set_page_config(
    page_title="Reporte Visiva",
    page_icon="📊",
    layout="wide", # que la layaut ocupe toda la pantalla
    initial_sidebar_state="collapsed"
)


#creamos la funcion de conexino a ala bd
@st.cache_resource(show_spinner=False)  # funcion decoradora para que la conxion se guarde en cache 
def get_connection(): # funcion para realizar y retornar la conexion
    return sqlitecloud.connect(
        "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
    )

# guardamos la conexino en una varible
con_sql = get_connection()
