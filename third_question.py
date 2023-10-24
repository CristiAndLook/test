import pandas as pd
import re
#Importar información 
df = pd.read_csv('./data/Question_3_data/question_3.csv')

#Pasamos los nombres a una lista
nombres = df['name'].tolist()

#Inicializar las listas
nueva_lista = []
lista_usuarios = []

#Inicializar los contadores 
contadores = [0, 0]

#Definir una función para procesar los nombres
def procesar_nombre(nombre):
    if re.search(r'[-./]', nombre):
        nombre_modificado = re.sub(r'[-./]', '', nombre)
        contadores[1] += 1
        return f'!subteam^{nombre_modificado}_{contadores[1]}'
    else:
        contadores[0] += 1
        lista_usuarios.append(f'@{nombre}_{contadores[0]}')
        return f'{nombre}_{contadores[0]}'

#Utilizar map para procesar los nombres
nueva_lista = list(map(procesar_nombre, nombres))

#Guardar las listas en un archivo .txt
with open('./nueva_lista.txt', 'w') as f:
    f.write(str(nueva_lista))

with open('./lista_usuarios.txt', 'w') as f:
    f.write(str(lista_usuarios))

# Imprimir las listas resultantes
print(f"Nueva Lista: {len(nueva_lista)}")
print(f"Lista de usuarios: {len(lista_usuarios)}")
print('Se crearon dos archivos: nueva_lista.txt y lista_usuarios.txt')