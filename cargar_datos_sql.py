import pandas as pd
import sqlitecloud

# Ruta del archivo Excel
excel_path = r"C:\Users\SCARBAJALR\Desktop\ProyectoVisiva\ProyectoVisivaRemoto\base_completa.xlsx"

# Conexión a la BD SQLite Cloud
conn = sqlitecloud.connect(
    "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
)

# Función para convertir columnas de fecha a texto ISO
def convert_date_columns(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

# Leer hojas
leads_df = pd.read_excel(excel_path, sheet_name='leads')
toques_df = pd.read_excel(excel_path, sheet_name='toques')

# Columnas fecha a convertir en leads
leads_date_cols = ['Fecha', 'Fecha Últ. Acción', 'primera_fecha_accion']

# Columnas fecha a convertir en toques (según tu tabla, solo 'fecha_ult_accion')
toques_date_cols = ['fecha_ult_accion']

# Convertir fechas a texto ISO
leads_df = convert_date_columns(leads_df, leads_date_cols)
toques_df = convert_date_columns(toques_df, toques_date_cols)

# Función para subir en chunks
def upload_in_chunks(df, table_name, conn, chunk_size=1000):
    for start in range(0, len(df), chunk_size):
        chunk = df.iloc[start : start + chunk_size]
        chunk.to_sql(table_name, conn, if_exists='append', index=False)
        print(f"Subido chunk filas {start} a {start + len(chunk)} a tabla {table_name}")

# Subir datos a SQLite Cloud
upload_in_chunks(leads_df, 'tb_leads', conn)
upload_in_chunks(toques_df, 'tb_toques', conn)
