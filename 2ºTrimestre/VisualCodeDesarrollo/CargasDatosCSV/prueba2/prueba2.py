import pandas as pd
import datapane as dp

# Cargar CSV
fichero_csv = "DI_U05_A02_PP_E_01.csv"
df = pd.read_csv(fichero_csv)

# Leer nombres de las columnas
df.columns = ["Año", "Región", "Tipo", "Ventas"]

# Tabla + DataTable
table = dp.Table(df)
data_table = dp.DataTable(df)

report = dp.Report(table, data_table)
report.save(path="informe_tablas.html", open=True)

# Cálculos del informe

# Total acumulado 2017 - 2021
total_acumulado = df["Ventas"].sum()

# Ventas por año
ventas_por_año = df.groupby("Año")["Ventas"].sum()

# Año con mayor volumen
año_max = ventas_por_año.idxmax()
importe_max = ventas_por_año.max()

# Ventas 2021 y 2020
ventas_2021 = ventas_por_año.get(2021, 0)
ventas_2020 = ventas_por_año.get(2020, 0)
diferencia = ventas_2021 - ventas_2020


# BigNumber resumen ejecutivo
resumen = dp.BigNumber(
    heading="Total ventas acumuladas (2017 - 2021)",
    value=total_acumulado,
    change=importe_max,
    is_upward_change=True
)


# BigNumber año con mayor volumen de ventas
anioMaxVolumen = dp.BigNumber(
    heading=f"Año con mayor volumen de ventas: {año_max}",
    value=importe_max,
    change=importe_max,
    is_upward_change=True
)


# BigNumber comparativa 2021 vs 2020
comparativa = dp.BigNumber(
    heading="Ventas 2021 vs 2020",
    value=ventas_2021,
    change=diferencia,
    is_upward_change=diferencia > 0
)

# Texto resumen ejecutivo con el año del mayor volumen de ventas.
texto_resumen = dp.Text(
    f"""
**Año con mayor volumen de ventas:** {año_max} ({importe_max} €)

Estos datos permiten a la dirección ver rápidamente el rendimiento global de la empresa,
identificar el mejor año y analizar qué factores influyeron en esos resultados.
"""
)

# Encabezado de la página
titulo = dp.HTML(
    '<p style="font-size:30px; text-align:center; color:#ffffff; background-color:#4d4d4d;">Informe de ventas</p>'
)

# Imagen de logotipo
imagen = dp.Media(file="ejercicio2.jpg")

# Adjuntar CSV para descargar
fichero = dp.Attachment(file=fichero_csv)

# Reporte final
report = dp.Report(
    imagen,
    titulo,
    dp.HTML("<h2>Resumen ejecutivo</h2>"),    
    resumen,
    comparativa,
    anioMaxVolumen,
    texto_resumen,
    data_table,
    fichero
)

report.save(path="Informe_Ventas_Final.html", open=True)
