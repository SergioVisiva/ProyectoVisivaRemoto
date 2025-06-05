import pandas as pd
import streamlit as st


def color_semaforo(val):
    if val > 3:
        color = 'background-color: lightgreen'
    elif val > 0:
        color = 'background-color: yellow'
    else:
        color = 'background-color: lightcoral'
    return color


# ejecuta la un query sql a la bd y nos retorna un df 
def ejecutar_consulta(con, query, params=None): # aparametros el objeto coneion , el query, parametros opcionales
    cursor = con.execute(query, params or ())  # el metodo execute del objeto conexion  crea un objeto cursor
    rows = cursor.fetchall()  # el metodo fetchall nos trae como lista de tuplas las filas  que el cursor consulto en la BD
    cols = [col[0] for col in cursor.description] # iteramos sobre la propiedad 'description' del objeto cursos, es propiedad es una lista de tuplas donde el primer elemeto de cada tupla es el nombre de cada columna de las los registros traidos por el cursor 
    return pd.DataFrame(rows, columns=cols) # creamos un objeto df con la clase 'Dataframe'  y sus atributos rows y cols
    # retornamos ese objeto df construido

def obtener_datos_filtrados_por_equipo(con, une):

    # SELECTOR DE EQUIPO
    status_query = """
                    SELECT 
                    DISTINCT Equipo 
                    FROM tb_toques
                    WHERE une = ?
                    """  # definimos el query
    df_status = ejecutar_consulta(con, status_query,  (une,)) # cramos un objeto df con la func 'ejecutar_consulta' y los parametros conexion y query
    opciones_equipo = ['-- Todos --'] + df_status['Equipo'].tolist() # usamos el meotodo "tolist" para converitr la serie seleccioanda en una lista
    selec_equipo = st.selectbox("Filtrar por Equipo", opciones_equipo, key=f'select_equipo_{une}') # creamos un dropdow con el metodo "selectbox" y la seleccion que se realize en pantalla se almacena en la varible "seleccion"


    query = """
    SELECT *
    FROM tb_toques
    WHERE une = ?
    AND (? = '-- Todos --' OR Equipo = ?)
    AND respuesta_ult_contacto IN ('Indeciso', 'Interesado', 'Quiere matricularse', 'Volver a llamar')
    """
    df_filtrado = ejecutar_consulta(con, query, (une, selec_equipo, selec_equipo)) #retornamos un objeto df con la func "ejecutar_consulta" cuyos parametros son la conexion, el query y los parametros los caules deben estan en un objeto iterable 

    # creamos la tabla pivotada con la funcion pivot_table de pandas
    tabla_pivot = pd.pivot_table(
        df_filtrado, # df que se usara como conjunto de datos
        #, "respuesta_ult_contacto"
        index=["ult_asesor"], #se agruapan por esos valores, esas agrupaciones pasan a ser indices de la nueva tabla
        columns="dia_mes_ultima_accion", # se indican que los valorres unicos d esa columna pasara a ser valores de columansa "el pivote"
        values="id_cliente", # los valors en los que se hara la agregacion
        aggfunc="count", # el tipo de agregacion
        fill_value=0 # si la agregacion para un conjunto de fila y columna es nulo se ponde cero
    ).reset_index() # los indices creados para la nueva tabla la convertimos otra ves en columnas

    st.subheader("📊 Tabla dinámica de contactos por día")

    columnas_dias = tabla_pivot.columns[2:] # guardamos en una varible el valor de las columnas pivotadas(dia)

    tabla_estilizada = tabla_pivot.style.applymap(color_semaforo, subset=columnas_dias) # accedemos al atributo style del objeto df, estto retorna un objeto y utlizimos su metodo "applymap" para dar estilo al df
    st.dataframe(tabla_estilizada, use_container_width=True) #renderizamos la tabla stilizada para mostrarlo en pantlla

    return tabla_pivot # retornamos la tabla para futuros calculo con el 
