import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def cargar_datos(file_path):
    dataset = pd.read_csv(file_path)
    return dataset

def limpiar_atributos(dataset):
    # Aquí puedes definir reglas de limpieza según el dataset específico
    dataset = dataset.dropna()  # Ejemplo: eliminar filas con valores nulos
    return dataset

def transformar_atributos_en_matriz(dataset, column_name='descripcion'):
    vectorizer = TfidfVectorizer(stop_words='english')
    matriz_caracteristicas = vectorizer.fit_transform(dataset[column_name])
    return matriz_caracteristicas


pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_rows', None)
print("Cargando datos...")
data = cargar_datos("data/data.csv")
print("Limpiando datos...")
data = limpiar_atributos(data)
print("Datos limpios:")

print(data)

print("Transformando datos...")
# matriz = transformar_atributos_en_matriz(data)
# print("Matriz de características:")
# print(matriz)