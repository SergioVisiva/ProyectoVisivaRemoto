import pandas as pd
import sqlitecloud

# Ruta del archivo Excel
excel_path = r"C:\Users\SCARBAJALR\Desktop\ProyectoVisiva\ProyectoVisivaRemoto\base_completa.xlsx"

# Conexión a la BD SQLite Cloud
conn = sqlitecloud.connect(
    "sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18"
)

def convert_date_columns(df, date_columns):
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%Y-%m-%d %H:%M:%S')
    return df

def clear_table(conn, table_name):
    conn.execute(f"DELETE FROM {table_name}")

def insert_rows_fast(df, table_name, conn, chunk_size=4000):
    cols = list(df.columns)
    insert_sql = f"INSERT INTO {table_name} ({', '.join(cols)}) VALUES ({','.join(['?'] * len(cols))})"
    data_iter = list(df.itertuples(index=False, name=None))

    conn.execute("BEGIN TRANSACTION;")
    for start in range(0, len(data_iter), chunk_size):
        conn.executemany(insert_sql, data_iter[start:start + chunk_size])
    conn.execute("COMMIT;")

# Cargar Excel y procesar
leads_df = pd.read_excel(excel_path, sheet_name='leads')
toques_df = pd.read_excel(excel_path, sheet_name='toques')

leads_df = convert_date_columns(leads_df, ['Fecha', 'Fecha_Ult_Accion', 'primera_fecha_accion'])
toques_df = convert_date_columns(toques_df, ['fecha_ult_accion'])

clear_table(conn, 'tb_leads')
insert_rows_fast(leads_df, 'tb_leads', conn)

clear_table(conn, 'tb_toques')
insert_rows_fast(toques_df, 'tb_toques', conn)

# Mensaje final
print("✅ Inserción completa de todos los datos en SQLite Cloud.")