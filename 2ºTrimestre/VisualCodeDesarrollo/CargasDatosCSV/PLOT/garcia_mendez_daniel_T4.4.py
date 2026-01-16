# garcia_mendez_daniel_T4.4.py
# Tarea 4.4 - Organización de componentes en Datapane
# Autor: Daniel García Méndez

import pandas as pd
import matplotlib.pyplot as plt
import datapane as dp

# 1. Cargar el fichero CSV
df = pd.read_csv("DI_U05_A02_PP_E_01.csv")

# 2. Crear tablas y gráficos

# Tabla completa
tabla_completa = dp.Table(df, label="Tabla completa")

# --- Gráfico 1: Ventas por año y región ---
ventas_anio_region = df.groupby(["Año", "Región"])["Ventas"].sum().reset_index()

fig1, ax1 = plt.subplots()
for region in ventas_anio_region["Región"].unique():
    datos_region = ventas_anio_region[ventas_anio_region["Región"] == region]
    ax1.bar(datos_region["Año"], datos_region["Ventas"], label=region)

ax1.set_title("Ventas por año y región")
ax1.set_xlabel("Año")
ax1.set_ylabel("Ventas")
ax1.legend()

grafico_anio_region = dp.Plot(fig1, label="Ventas por año y región")

# --- Gráfico 2: Ventas por año y tipo de producto ---
ventas_anio_producto = df.groupby(["Año", "Tipo de producto"])["Ventas"].sum().reset_index()

fig2, ax2 = plt.subplots()
for tipo in ventas_anio_producto["Tipo de producto"].unique():
    datos_tipo = ventas_anio_producto[ventas_anio_producto["Tipo de producto"] == tipo]
    ax2.plot(datos_tipo["Año"], datos_tipo["Ventas"], marker="o", label=tipo)

ax2.set_title("Ventas por año y tipo de producto")
ax2.set_xlabel("Año")
ax2.set_ylabel("Ventas")
ax2.legend()

grafico_anio_producto = dp.Plot(fig2, label="Ventas por año y tipo de producto")

# Tabla resumen por tipo de producto
tabla_resumen_producto = dp.Table(
    ventas_anio_producto,
    label="Resumen por año y tipo de producto"
)

# 3. GRUPO (tabla + gráfico)
grupo_resumen = dp.Group(
    tabla_completa,
    grafico_anio_region,
    columns=2
)

# 4. SELECTOR (dos gráficos alternativos)
selector_graficos = dp.Select(
    blocks=[
        grafico_anio_region,
        grafico_anio_producto
    ]
)

# 5. PÁGINAS
pagina_1 = dp.Page(
    title="Resumen general",
    blocks=[
        dp.Text("# Informe de ventas por región y producto"),
        dp.Text(
            "En esta página se muestra una visión general de los datos: "
            "la tabla completa y un gráfico de ventas por año y región."
        ),
        grupo_resumen
    ]
)

pagina_2 = dp.Page(
    title="Análisis detallado",
    blocks=[
        dp.Text("## Comparación de vistas"),
        dp.Text(
            "Utiliza el selector para alternar entre diferentes vistas de las ventas: "
            "por región o por tipo de producto."
        ),
        selector_graficos,
        dp.Text("## Resumen por año y tipo de producto"),
        tabla_resumen_producto
    ]
)

# 6. Informe final
informe = dp.Report(
    pagina_1,
    pagina_2
)

# 7. Guardar HTML
informe.save(path="garcia_mendez_daniel_T4.4.html")

print("Informe generado correctamente: garcia_mendez_daniel_T4.4.html")
