import pandas as pd
import plotly.express as px

# Datos de ejemplo
data = {
    'País': ['Perú', 'Perú', 'Perú', 'Chile', 'Chile', 'Chile'],
    'Departamento': ['Lima', 'Cusco', 'Arequipa', 'Santiago', 'Valparaíso', 'Antofagasta'],
    'Año': [2022, 2022, 2022, 2022, 2022, 2022],
    'Exportaciones': [1000, 500, 700, 1200, 800, 600]
}
df = pd.DataFrame(data)

# Pivot para tener los años como columnas
pivot_df = df.pivot_table(index=['País', 'Departamento'], columns='Año', values='Exportaciones', aggfunc='sum').reset_index()

# Tabla jerárquica interactiva con expansión
fig = px.treemap(
    df,
    path=['País', 'Departamento'],
    values='Exportaciones',
    color='Exportaciones',
    title='Exportaciones por País y Departamento'
)
fig.show()
