import pandas as pd
import sqlitecloud

# Ruta del archivo Excel
ruta_excel = r"C:\Users\SCARBAJALR\Desktop\ProyectoVisiva\ProyectoVisivaRemoto\base_completa.xlsx"

# Cargar las hojas del Excel en DataFrames
leads_df = pd.read_excel(ruta_excel, sheet_name="leads")
toques_df = pd.read_excel(ruta_excel, sheet_name="toques")

# String de conexión a SQLite Cloud
conn_string = "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"

# Conectar a la base
conn = sqlitecloud.connect(conn_string)

def upload_in_chunks(df, table_name, conn, chunk_size=1000):
    # Eliminar tabla si existe
    with conn:
        conn.execute(f"DROP TABLE IF EXISTS {table_name};")

    # Subir por partes
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i+chunk_size]
        chunk.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Subido chunk filas {i} a {i + len(chunk)} a tabla {table_name}")

# Subir datos
upload_in_chunks(leads_df, "tb_leads", conn)
upload_in_chunks(toques_df, "tb_toques", conn)

print("Carga finalizada.")
