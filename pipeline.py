import pandas as pd
import streamlit as st
import sqlite3

def color_semaforo(val):
    if val > 5:
        color = 'background-color: lightgreen'
    elif val > 2:
        color = 'background-color: yellow'
    else:
        color = 'background-color: lightcoral'
    return color

def obtener_datos_filtrados_por_equipo(con, pagina):
    st.title(f"Reporte de: {pagina}")

    status_query = "SELECT DISTINCT Equipo FROM tb_toques"
    df_status = pd.read_sql_query(status_query, con)
    opciones_equipo = df_status['Equipo'].tolist()

    seleccion = st.selectbox("Filtrar por Equipo", opciones_equipo)

    query = """
    SELECT *
    FROM tb_toques
    WHERE Equipo = ?
    """
    df_filtrado = pd.read_sql_query(query, con, params=(seleccion,))

    tabla_pivot = pd.pivot_table(
        df_filtrado,
        index=["ult_asesor", "respuesta_ult_contacto"],
        columns="dia_mes_ultima_accion",
        values="id_cliente",
        aggfunc="count",
        fill_value=0
    ).reset_index()

    st.subheader("📊 Tabla dinámica de contactos por día")

    columnas_dias = tabla_pivot.columns[2:]

    tabla_estilizada = tabla_pivot.style.applymap(color_semaforo, subset=columnas_dias)

    st.dataframe(tabla_estilizada, use_container_width=True)

    return tabla_pivot

if __name__ == "__main__":
    con = sqlite3.connect("tu_basededatos.sqlite")  # Cambia por tu BD
    pagina = "Equipo XYZ"
    obtener_datos_filtrados_por_equipo(con, pagina)
