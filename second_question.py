import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#Importar información de las ciudades
ciudades = pd.read_csv('./data/Question_2_data/question_2_part1.csv')

#Importar información de los pedidos
ordenes = pd.read_csv('./data/Question_2_data/question_2.csv')

#Función para verificar si una orden viola las restricciones de la ciudad
def is_order_violating_restriction(order):
    city_id = order['city_address_id']
    start_time, end_time = city_intervals.get(city_id, (None, None))
    if start_time and end_time:
        order_time = order['created_at'].time()
        if start_time <= end_time:
            return not (start_time <= order_time <= end_time)
        else:
            return order_time < start_time and order_time > end_time
    return False

#Convertir la columna 'created_at' a tipo datetime
ordenes['created_at'] = pd.to_datetime(ordenes['created_at'])

#Crear un diccionario con los intervalos de tiempo para cada ciudad esto lo usara la función
city_intervals = dict(zip(ciudades['city_address_id'], ciudades.apply(lambda row: (pd.to_datetime(row['starts_at'], format='%H:%M:%S').time(), pd.to_datetime(row['ends_at'], format='%H:%M:%S').time()), axis=1)))

#Aplicar la función para encontrar las órdenes que violan las restricciones
violating_orders = ordenes[ordenes.apply(is_order_violating_restriction, axis=1)]

print(f'\nCantidad de órdenes que violan las restricciones: {len(violating_orders)}')
#Se genera un archivo .csv con las órdenes que violan las restricciones
print(f'\nSe generó un archivo .csv con las órdenes que violan las restricciones\n')
violating_orders.to_csv('./violating_orders.csv', index=False) 

#Contar las órdenes por city_address_id
order_counts = violating_orders['city_address_id'].value_counts().reset_index()
order_counts.columns = ['city_address_id', 'order_count']

#Mostrar los resultados por consola
print(f'\nCantidad de órdenes que violan las restricciones agrupados por city_address_id:\n')
print(order_counts)