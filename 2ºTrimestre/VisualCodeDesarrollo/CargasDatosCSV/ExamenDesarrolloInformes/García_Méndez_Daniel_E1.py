import pandas as pd
import datapane as dp
import matplotlib.pyplot as plt

fichero_cvs ="uso_servicios_municipales.csv"

df = pd.read_csv(fichero_cvs)


# mayor_numero_servicios = df.groupby("anio")["numero_usos"].sum().head(1)

tabla_interactiva = dp.DataTable(df)

# CREACIÓN DEL REPORTE CON LA TABLA INTERACTIVA
informe1 = dp.Report(tabla_interactiva)
informe1.save("garcia_mendez_daniel_E1_tabla.html",open = False)