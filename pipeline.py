import streamlit as st
import pandas as pd
import sqlitecloud

# Conexión a la BD SQLite Cloud
conn = sqlitecloud.connect(
    "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
)

# Consulta SQL para traer datos (ejemplo desde tb_leads)
query = "SELECT * FROM tb_leads LIMIT 1000"
df = pd.read_sql_query(query, conn)

st.title("Reporte Básico - Leads")

st.dataframe(df)

conn.close()
