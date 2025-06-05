import streamlit as st
import pandas as pd
from io import BytesIO
import re
import datetime as dt

def app_hsm():
    st.title("📤 Cargar y procesar Bases HSM")
    st.write("Cargue un archivo por curso.")

    # 🔄 Botón para reiniciar
    if st.button("🔄 Reiniciar carga"):
        st.session_state["archivos_cargados"] = []
        st.rerun()

    # 2️⃣ ¿Cuántos registros deseas por curso?
    reg_solicitado = st.number_input("¿Cuántos registros deseas por curso?", min_value=1, value=400)

    # 📎 Uploader controlado
    archivos = st.file_uploader("📎 Carga tu archivo Excel", type=["xlsx", "xls"], accept_multiple_files=True)

    # Guardamos en session_state si hay carga
    if archivos:
        st.session_state["archivos_cargados"] = archivos

    # Recuperamos desde session_state
    archivos_cargados = st.session_state.get("archivos_cargados", [])




    # 🧹 Función para limpiar archivos
    def Limpieza(df, n):
        df['fecha_ult_accion'] = pd.to_datetime(df['fecha_ult_accion'], errors='coerce')
        df = df.dropna(subset=['fecha_ult_accion'])

        idx = df.groupby('id_cliente')['fecha_ult_accion'].idxmax()
        df = df.loc[idx]

        df['celular'] = df['celular'].astype(str).str.strip()
        df = df[~df['celular'].str.startswith('0')]
        df['celular'] = pd.to_numeric(df['celular'], errors='coerce')
        df = df.dropna(subset=['celular'])
        df['celular'] = df['celular'].astype(int)
        df = df[df['celular'].astype(str).str.match(r'^9\d{8}$')]

        df = df.sort_values(by='fecha_ult_accion', ascending=False)
        if n:
            df = df.head(n)

        curso = df['programa'].iloc[0] if not df.empty else "Desconocido"
        cant_reg_retorno = len(df)
        
        return df, curso, cant_reg_retorno


    # Procesar archivos si hay cargados
    list_df_limpio = []
    for archivo in archivos_cargados:
        try:
            df = pd.read_excel(archivo)
            df_limpio, curso, cant_reg_retorno = Limpieza(df, reg_solicitado)
            list_df_limpio.append({
                'df': df_limpio,
                'curso': curso,
                'cant_reg_retorno': cant_reg_retorno
            })
        except Exception as e:
            st.error(f"❌ Error procesando archivo {archivo.name}: {e}")

    # Mostrar resultados y permitir descarga
    if list_df_limpio:
        st.subheader("📊 Cursos procesados")

        for item in list_df_limpio:
            st.markdown(f"""
            - **Curso**: `{item['curso']}`
            - **Registros**: `{item['cant_reg_retorno']}`
            """)

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            for item in list_df_limpio:
                nom_hoja = re.sub(r'[:\\/*?\[\]]', '', item['curso'])[:31]
                item['df'].to_excel(writer, sheet_name=nom_hoja, index=False)
        output.seek(0)

        st.download_button(
            label="📥 Descargar Base",
            data=output,
            file_name=f"Bases_{dt.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )