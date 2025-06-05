import streamlit as st
import Pipeline as pv 
import configuracion as cv
import hsm as hsm

# BARRA LATERAL
st.sidebar.header("Navegación")
opciones = ["📋 Pipeline", "📈 Base Gestionable", "🗂️ Bases HSM"]
pagina = st.sidebar.radio("Selecciona la página:", opciones)
st.session_state.pagina = pagina


#--- PANTALLA
if pagina == "🗂️ Bases HSM":
    hsm.app_hsm()


# Solo si estamos en Pipeline
elif pagina == "📋 Pipeline":
    une = st.radio("Seleccione la UNE", ["UCAL", "TLS", "CERTUS"], horizontal=True)
    
    pv.obtener_datos_filtrados_por_equipo(cv.con_sql, une)
    # Selector principal al centro superior
    



