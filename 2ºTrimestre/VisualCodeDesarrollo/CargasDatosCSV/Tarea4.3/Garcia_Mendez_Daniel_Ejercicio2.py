import pandas as pd
import matplotlib.pyplot as plt
import datapane as dp

# Cargar datos
df = pd.read_csv("DI_U05_A02_PP_E_01.csv")

# 1. GRÁFICO DE TARTA
ventas_por_tipo = df.groupby("Tipo de producto")["Ventas"].sum()

grafico_tarta = ventas_por_tipo.plot.pie(
    ylabel="",
    legend=False,
    title="Distribución de ventas por tipo de producto"
)

grafico_datapane = dp.Plot(grafico_tarta)
plt.close()

# 2. GRÁFICO DE LÍNEAS (últimos 2 años)
ventas_anuales = df.groupby("Año")["Ventas"].sum()
ventas_de_dos_anios = ventas_anuales.tail(2)


grafico_lineas = ventas_de_dos_anios.plot.line(
    ylabel="Ventas totales",
    xlabel="Año",
    title="Evolución de ventas totales (últimos 2 años)"
)

grafico_lineas_datapane = dp.Plot(grafico_lineas)
plt.close()

# 3. GRÁFICO DE BARRAS POR REGIÓN
ventas_totales_por_region = df.groupby("Región")["Ventas"].sum()
grafico_matplotlib_Barras = ventas_totales_por_region.plot.bar(y= "Región")

graficoData = dp.Plot(grafico_matplotlib_Barras)
plt.close()

titulo = dp.HTML(
    '<h1 style="font-size:30px; text-align:center; color:#ffffff; background-color:#4d4d4d;">'
    'Informe de ventas '
    '</h1>'
)

# 3. INFORME
reporte = dp.Report(
    titulo,
    dp.Text("# Distribución de ventas por tipo de producto"),
    grafico_datapane,
    dp.Text("# Evolución de ventas en los últimos 2 años"),
    grafico_lineas_datapane,
    dp.Text("# Evolución de ventas en las diferentes regiones"),
    graficoData
)

reporte.save("informe_ventas_por_tipo.html", open=True)
