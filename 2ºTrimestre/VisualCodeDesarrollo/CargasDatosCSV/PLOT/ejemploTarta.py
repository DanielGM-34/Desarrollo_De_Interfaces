import pandas as pd
import datapane as dp

# Cargar los datos desde el CSV
df = pd.read_csv("DI_U05_A02_02.csv")

# Agrupar por vendedor y sumar (para obtener los totales)
ventas_vendedor = df.groupby(["Nombre"]).sum()

# Crear el gráfico de sectores (tarta)
grafico_matplotlib = ventas_vendedor.plot.pie(
    y="Unidades",
    legend=False,
    ylabel=""
)

# Adaptar el gráfico para Datapane
grafico_datapane = dp.Plot(grafico_matplotlib)

# Crear el informe Datapane
reporte = dp.Report(
    dp.Text("# Reparto de unidades vendidas por vendedor"),
    grafico_datapane
)

# Guardar y abrir el informe
reporte.save("informe_reparto_unidades.html", open=True)