import pandas as pd
import sqlitecloud

# Ruta al archivo Excel
excel_path = r"C:\Users\SCARBAJALR\Desktop\ProyectoVisiva\ProyectoVisivaRemoto\base_completa.xlsx"

# Leer las hojas del Excel
leads_df = pd.read_excel(excel_path, sheet_name='leads')
toques_df = pd.read_excel(excel_path, sheet_name='toques')

# Conectarse a la base SQLite en la nube
conn = sqlitecloud.connect("sqlitecloud://cvixcqxfnz.g3.sqlite.cloud:8860/dbVisiva?apikey=Duup7ZbjbIH5w0TFTj9MewoF4GnD8KtGayXaDDOEy18")

# Cargar las hojas a tablas
leads_df.to_sql("leads", conn, if_exists="replace", index=False)
toques_df.to_sql("toques", conn, if_exists="replace", index=False)

print("✅ Datos cargados correctamente a la base SQLite en la nube.")
conn.close()
