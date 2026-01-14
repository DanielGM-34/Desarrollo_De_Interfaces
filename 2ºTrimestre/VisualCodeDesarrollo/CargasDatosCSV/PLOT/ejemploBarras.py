import pandas as pd
import datapane as dp

# Cargar los datos desde el CSV
df = pd.read_csv("DI_U05_A02_02.csv")

# Agrupar los datos por vendedor y sumar los importes
ventas_vendedor = df.groupby(["Nombre"]).sum()

# Crear el gráfico de barras (Pandas usa Matplotlib internamente)
grafico_matplotlib = ventas_vendedor.plot.bar(y="Importe (€)")

# Adaptar el gráfico para Datapane
grafico_datapane = dp.Plot(grafico_matplotlib)

# Crear el informe Datapane
reporte = dp.Report(
    dp.Text("# Ventas por vendedor"),
    grafico_datapane
)

# Guardar y abrir el informe
reporte.save("informe_ventas_vendedor.html", open=True)