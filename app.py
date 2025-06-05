import streamlit as st
import sqlitecloud
import pandas as pd

def obtener_datos():
    connection_string = "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
    conn = sqlitecloud.connect(connection_string)
    
    # Ejecutar consulta y cargar en pandas DataFrame
    cursor = conn.execute("SELECT * FROM tb_toques")  # Cambia tb_toques por tu tabla real
    rows = cursor.fetchall()
    columns = [col[0] for col in cursor.description]  # Obtener nombres columnas
    
    conn.close()
    
    df = pd.DataFrame(rows, columns=columns)
    return df

st.title("Dashboard con datos SQLite Cloud")

try:
    df = obtener_datos()
    st.dataframe(df)  # Muestra DataFrame en Streamlit
except Exception as e:
    st.error(f"Error al obtener datos: {e}")


