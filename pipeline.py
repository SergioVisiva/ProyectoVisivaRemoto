import pandas as pd
import streamlit as st
import sqlite3  
from st_aggrid import AgGrid, GridOptionsBuilder
import streamlit as st
import pandas as pd

def obtener_datos_filtrados_por_equipo(con, pagina):


    # Título dinámico según la página
    st.title(f"Reporte de : {pagina}")

    # Obtener equipos disponibles
    status_query = "SELECT DISTINCT Equipo FROM tb_toques"
    df_status = pd.read_sql_query(status_query, con)
    opciones_equipo = df_status['Equipo'].tolist()

    # Selector en la barra lateral
    seleccion = st.selectbox("Filtrar por Equipo", opciones_equipo)

    # Query filtrado
    query = """
    SELECT * FROM tb_toques
    WHERE Equipo = ?
    """
    df_filtrado = pd.read_sql_query(query, con, params=(seleccion,))

    # Mostrar resultados
    #st.dataframe(df_filtrado)
    


    # Configuración de AgGrid
    gb = GridOptionsBuilder.from_dataframe(df_filtrado)

    # AREA DE FILAS (jerarquía): Producto y Subproducto
    gb.configure_column("ult_asesor", rowGroup=True, hide=True)
    gb.configure_column("respuesta_ult_contacto", rowGroup=True, hide=True)

    # 🔸 AREA DE COLUMNAS: Zona
    gb.configure_column("dia_mes_ultima_accion", pivot=True)

    # 🔸 AREA DE VALORES: Ventas
    gb.configure_column("id_cliente", aggFunc="count")

    # Otras opciones
    gb.configure_default_column(groupable=True, enableValue=True, enableRowGroup=True, enablePivot=True)

    gridOptions = gb.build()

    # Mostrar tabla dinámica
    AgGrid(
        df_filtrado,
        gridOptions=gridOptions,
        enable_enterprise_modules=True,
        fit_columns_on_grid_load=True
    )

    

    return df_filtrado
