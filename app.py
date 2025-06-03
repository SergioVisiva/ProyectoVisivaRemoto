from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

# Data ejemplo
data = {
    'ult_asesor': ['Juan', 'Juan', 'Ana', 'Ana'],
    'respuesta_ult_contacto': ['OK', 'Pendiente', 'OK', 'Pendiente'],
    'dia_mes_ultima_accion': ['2025-06-01', '2025-06-02', '2025-06-01', '2025-06-02'],
    'id_cliente': [1, 2, 3, 4]
}
df = pd.DataFrame(data)

gb = GridOptionsBuilder.from_dataframe(df)

# Configurar filas agrupadas
gb.configure_column("ult_asesor", rowGroup=True, hide=True)
gb.configure_column("respuesta_ult_contacto", rowGroup=True, hide=True)

# Configurar columna pivot (columnas dinámicas)
gb.configure_column("dia_mes_ultima_accion", pivot=True)

# Configurar valor a contar
gb.configure_column("id_cliente", aggFunc='count')

gb.configure_default_column(groupable=True, enableRowGroup=True, enablePivot=True, enableValue=True)

gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True)
