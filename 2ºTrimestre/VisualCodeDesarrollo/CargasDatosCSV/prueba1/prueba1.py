import pandas as pd
import datapane as dp

# 1) Cargar CSV y renombrar columna

fichero_csv = "DI_U05_A02_02.csv"
df = pd.read_csv(fichero_csv)

df = df.rename(columns={"Importe (€)": "Importe"})

# 2) FILTRADOS DEL EJERCICIO 1

# 1. Vendedores en julio con >500 unidades
ej1_julio = df[(df['Mes'] == 'Julio') & (df['Unidades'] > 500)]
big_julio = dp.BigNumber(
    heading="Vendedores en julio con >500 unidades",
    value=f"{len(ej1_julio)} Unidades" 
)

# 2. Mayor importe con ≤300 unidades
ej1_importe = df[df['Unidades'] <= 300].sort_values(by="Importe", ascending=False).head(1)
big_importe = dp.BigNumber(
    heading="Importe máximo con ≤300 unidades",
    value=float(ej1_importe["Importe"].iloc[0])
)

# 3. Vendedores que empiezan por S en agosto
ej1_agosto_s = df[(df["Mes"] == "Agosto") & (df["Nombre"].str.startswith("S"))]
ej1_agosto_s = ej1_agosto_s.sort_values(by="Unidades", ascending=False).head(1)


big_agosto_s = dp.BigNumber(
    heading="Máximo vendedor 'S' en agosto",
    value=int(ej1_agosto_s["Unidades"].iloc[0])
)

# Tablas individuales (solo las filtradas)
tabla_julio = dp.DataTable(ej1_julio)
tabla_importe = dp.DataTable(ej1_importe)
tabla_agosto_s = dp.DataTable(ej1_agosto_s)

# 3) Elementos visuales del informe

titulo = dp.HTML(
    '<p style="font-size:30px; text-align:center; color:#ffffff; background-color:#4d4d4d;">'
    'Ejercicio 1 – Filtrado y análisis de ventas'
    '</p>'
)

texto = dp.Text("**Resultados obtenidos aplicando filtros y ordenaciones con DataTable.**")
fichero = dp.Attachment(file='DI_U05_A02_02.csv')

# 4) INFORME ÚNICO FINAL (SOLO FILTROS) AQUÍ SALEN LAS TABLAS CON TODOS LOS FILTROS APLICADOS.

report = dp.Report(
    titulo,
    dp.Group(big_julio, big_importe, big_agosto_s, columns=3),

    dp.Text("### Resultado 1: Julio > 500 unidades"),
    tabla_julio,

    dp.Text("### Resultado 2: Importe máximo con ≤300 unidades"),
    tabla_importe,

    dp.Text("### Resultado 3: Vendedores que empiezan por S en agosto"),
    tabla_agosto_s,

    texto,
    fichero
)

report.save(path="DI_U05_A02_03_EJ1_FINAL.html", open=True)
