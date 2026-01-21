import pandas as pd
import datapane as dp
import matplotlib.pyplot as plt  # Importación estándar

# 1. CARGA DEL MODELO
df = pd.read_csv("DI_U05_A02_PP_E_01.csv")
df.columns = df.columns.str.lower()

# 2. CÁLCULO DE INDICADORES

# Ventas totales en todo el periodo
total_ventas = df["ventas"].sum()

# Ventas totales en el último año (2021)
ventas_2021 = df[df["año"] == 2021]["ventas"].sum()

# Producto con más ventas totales
ventas_por_producto = df.groupby("tipo de producto")["ventas"].sum()
producto_top = ventas_por_producto.idxmax()
ventas_producto_top = ventas_por_producto.max()

# 3. ELABORACIÓN DE GRÁFICOS

# --- Gráfico 1: Barras apiladas por AÑO y TIPO DE PRODUCTO ---
plt.figure()
ventas_año_producto = df.groupby(["año", "tipo de producto"])["ventas"].sum().unstack()
plot1 = ventas_año_producto.plot(kind="bar", title="Ventas por Año y Producto")
bloque_bar_apilado = dp.Plot(plot1.get_figure(), label="Año vs Producto")

# --- Gráfico 2: Barras por REGIÓN y AÑO ---
plt.figure()
ventas_region_año = df.groupby(["región", "año"])["ventas"].sum().unstack()
plot2 = ventas_region_año.plot(kind="bar", title="Ventas por Región y Año")
bloque_bar_region = dp.Plot(plot2.get_figure(), label="Región vs Año")

# --- Gráfico 3: Líneas de evolución total por AÑO ---
plt.figure()
ventas_año = df.groupby("año")["ventas"].sum()
plot3 = ventas_año.plot(kind="line", marker="o", title="Evolución Total de Ventas")
bloque_linea = dp.Plot(plot3.get_figure(), label="Evolución Temporal")

# 4. ORGANIZACIÓN DEL INFORME

# Página 1: Dashboard Principal con indicadores y gráfico
pagina1 = dp.Page(
    title="Dashboard",
    blocks=[
        dp.Text("# Resumen de Ventas"),
        dp.Group(
            dp.BigNumber(heading="Ventas Totales (2017–2021)", value=f"{total_ventas:,.0f} €"),
            dp.BigNumber(heading="Ventas en 2021", value=f"{ventas_2021:,.0f} €"),
            columns=2
        ),
        dp.BigNumber(
            heading="Producto más vendido (total periodo)",
            value=f"{producto_top} ({ventas_producto_top:,.0f} €)"
        ),
        bloque_linea
    ]
)

# Página 2: Comparativas con Selectores
pagina2 = dp.Page(
    title="Comparativas",
    blocks=[
        dp.Text("# Comparativas por Año, Producto y Región"),
        dp.Select(
            blocks=[
                bloque_bar_apilado,
                bloque_bar_region
            ]
        )
    ]
)

# Página 3: Explorador de Datos
pagina3 = dp.Page(
    title="Datos",
    blocks=[
        dp.Text("# Tabla Completa de Registros"),
        dp.DataTable(df)
    ]
)

# 5. GENERACIÓN FINAL
reporte = dp.Report(pagina1, pagina2, pagina3)
reporte.save("garcia_mendez_daniel_T4.4.html", open=True)