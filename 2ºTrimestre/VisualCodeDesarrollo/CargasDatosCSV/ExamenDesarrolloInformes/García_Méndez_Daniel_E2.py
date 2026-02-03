import pandas as pd
import datapane as dp
import matplotlib.pyplot as plt

fichero_cvs ="uso_servicios_municipales.csv"

df = pd.read_csv(fichero_cvs)

# SUME TOTAL DE NUMERO DE USOS
usosTotales=df["numero_usos"].sum()

# BIGNUMBER CON EL TOTAL DE USOS ACUMULADOS
total_usos_acumulados=dp.BigNumber(
    heading="Total de usos",
    value=usosTotales
    )

# COMPARACIÓN DE NÚMERO DE USOS ENTRE LOS AÑOS 2022 Y 2023
filtrar_Anio2023 = df[df["anio"] == 2023]["numero_usos"].sum()
filtrar_Anio2022 = df[df["anio"] == 2022]["numero_usos"].sum()

# BIGNUMBER CON LA COMPARATIVA DE LOS DOS AÑOS 
comparacion_anios=dp.BigNumber(
    heading="COMPARATIVA ENTRE NÚMEROS DE USOS ENTRE 2023 Y 2022",
    value=filtrar_Anio2023 - filtrar_Anio2022
    ,
    is_upward_change=True
    ,
    change=usosTotales
)

# CREACIÓN DEL INFORME 2
informe2 = dp.Report(
    dp.HTML("**Resumen uso ejecutivo - Uso de servicios municipales**"), 
    dp.Text("este resumen es muy importante, ya que puedes ver un resumen general de un total de usos acumulados con la comparación")
    ,
            total_usos_acumulados,comparacion_anios
            ) 

informe2.save("garcia_mendez_daniel_E2_resumen.html",open=False)