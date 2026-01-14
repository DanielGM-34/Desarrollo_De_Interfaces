import pandas as pd
import datapane as dp

# Cargar los datos desde el CSV
df = pd.read_csv("DI_U05_A02_02.csv")

# Agrupar los datos por mes y sumar las unidades vendidas
ventas_mes = df.groupby(["Mes"], sort=False).sum()

# Crear el gráfico de líneas (Matplotlib a través de Pandas)
grafico_matplotlib = ventas_mes.plot(y="Unidades")

# Adaptar el gráfico para Datapane
grafico_datapane = dp.Plot(grafico_matplotlib)

reporte = dp.Report(
    dp.Text("# Informe de ventas"),
    grafico_datapane
)

reporte.save("informe_ventas.html", open=True)