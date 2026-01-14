import pandas as pd
import datapane as dp

# Cargar los datos desde el CSV
df = pd.read_csv("DI_U05_A02_02.csv")

# Preparar datos: unidades totales por mes
ventas_mes = df.groupby(["Mes"], sort=False).sum()

# Crear el gráfico (Pandas usa Matplotlib internamente)
grafico_matplotlib = ventas_mes.plot(y="Unidades")

# Adaptar gráfico a Datapane
bloque_grafico = dp.Plot(grafico_matplotlib)

# Crear una tabla con los datos agregados
tabla_resumen = dp.DataTable(ventas_mes)

# Construir el informe completo
reporte = dp.Report(
    dp.Text("# Panel de ventas"),
    dp.Text("Este panel muestra la evolución mensual de las unidades vendidas y el resumen por mes."),
    bloque_grafico,
    dp.Text("## Detalle por mes"),
    tabla_resumen
)

# Guardar y abrir el informe
reporte.save("panel_ventas_mensual.html", open=True)