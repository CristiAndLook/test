#Importar librerias
import pandas as pd
import os
from datetime import datetime, timedelta

#Declaramos las funciones
#Función para importar archivos CSV desde una ruta 
def importar_archivos_csv_desde_ruta(ruta_carpeta, ultimo_archivo_leido=None):
    #Si la variable 'ultimo_archivo_leido' está definida, encuentra su índice en la lista de archivos
    if ultimo_archivo_leido:
        try:
            indice_inicio = os.listdir(ruta_carpeta).index(ultimo_archivo_leido)
        except ValueError:
            #El archivo anteriormente leído ya no existe, comienza desde el principio
            indice_inicio = 0
    else:
        #Si 'ultimo_archivo_leido' no está definido, comienza desde el principio
        indice_inicio = 0

    #Inicializa una lista vacía para almacenar los DataFrames individuales
    dataframes = []

    #Recorre los archivos a partir del índice calculado
    archivos = os.listdir(ruta_carpeta)
    for i in range(indice_inicio, len(archivos)):
        archivo = archivos[i]
        if archivo.endswith(".csv"):
            ruta_completa = os.path.join(ruta_carpeta, archivo)
            #Lee cada archivo CSV y agrega su contenido a la lista
            df = pd.read_csv(ruta_completa)
            dataframes.append(df)
            #Actualiza la variable 'ultimo_archivo_leido'
            ultimo_archivo_leido = archivo

    #Concatena todos los DataFrames en uno solo
    datos_completos = pd.concat(dataframes, ignore_index=True)

    #Devuelve el DataFrame con los datos y el nombre del último archivo leído
    return datos_completos, ultimo_archivo_leido

#Uso de la función
ruta_carpeta = "./data/Question_1_data"  # Reemplaza con la ruta correcta en tú sistema
datos_completos, ultimo_archivo_leido = importar_archivos_csv_desde_ruta(ruta_carpeta)

#Modificamos el formato de fecha del dataframe y trabajamos con los datos faltantes
df = datos_completos

#Convertir la columna Timestamp a tipo datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

#Llena los campos NaT con la fecha del campo anterior + 1 segundo
for index, row in df.iterrows():
    if pd.isna(row['timestamp']):
        df.at[index, 'timestamp'] = df.at[index - 1, 'timestamp'] + pd.Timedelta(seconds=1)

#Filtramos el dataframe solo con los order_id que tienen un evento "payless_barcodes_created" y ordenamos por 'order_id' y 'timestamp'
#para poder calcular la diferencia de tiempo entre eventos consecutivos para cada order_id
#Al no tener claro que dispara el evento "payless_barcodes_created" se da una solución general. 

#Filtrar los eventos "payless_barcodes_created"
payless_events = df[df['name'] == 'payless_barcodes_created']

#Crear una lista para almacenar los DataFrames individuales
result_dfs = []

#Iterar a través de los eventos "payless_barcodes_created"
for index, row in payless_events.iterrows():
    order_id = row['order_id']

    # Filtrar todas las coincidencias para el mismo order_id
    order_events = df[df['order_id'] == order_id]

    result_dfs.append(order_events)

#Concatenar los DataFrames individuales en un solo DataFrame
result_df = pd.concat(result_dfs, ignore_index=True)

#Ordenar el DataFrame por 'order_id' y 'timestamp'
df = result_df.sort_values(by=['order_id', 'timestamp'])

#Crear una columna 'diferencia' para calcular la diferencia de tiempo entre eventos consecutivos
df['diferencia'] = df.groupby('order_id')['timestamp'].diff()

#Encontrar los pedidos que demoraron más de 50 segundos en generar el evento 'payless_barcodes_created'
pedidos_con_demora = df[(df['name'] == 'payless_barcodes_created') & (df['diferencia'] > pd.Timedelta('50 seconds'))]

#Obtener la lista de los pedidos que cumplieron con la condición
pedidos_demorados = pedidos_con_demora['order_id'].unique()

#Mostrar los resultados por consola
print(f'Pedidos que POSIBLEMENTE demoraron MÁS DE 50 segundos en generar "payless_barcodes_created":\n')
[print(pedido) for pedido in pedidos_demorados]



