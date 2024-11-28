import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import scipy.sparse

# Cargar los datos
def cargar_datos(ruta):
    """
    Carga el dataset desde un archivo CSV.
    :param ruta: Ruta del archivo CSV
    :return: DataFrame de pandas
    """
    try:
        df = pd.read_csv(ruta)
        print("Archivo cargado exitosamente.")
        return df
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo en la ruta: {ruta}")
        return None

# Limpieza y procesamiento del texto
def limpiar_datos(df):
    """
    Limpia y prepara los datos del DataFrame.
    :param df: DataFrame con los datos de los cursos
    :return: DataFrame procesado
    """
    if "descripcion" not in df.columns:
        print("Error: La columna 'descripcion' no se encuentra en el archivo.")
        return None
    df["descripcion"] = df["descripcion"].fillna("").str.lower()
    print("Datos limpiados y procesados.")
    return df

# Transformar descripciones en una matriz TF-IDF
def generar_matriz_caracteristicas(df):
    """
    Genera la matriz de características basada en TF-IDF.
    :param df: DataFrame con descripciones de los cursos
    :return: Matriz TF-IDF y vectorizador
    """
    try:
        vectorizador = TfidfVectorizer(stop_words="english")
        matriz = vectorizador.fit_transform(df["descripcion"])
        print("Matriz TF-IDF generada con éxito.")
        return matriz, vectorizador
    except Exception as e:
        print(f"Error al generar la matriz TF-IDF: {e}")
        return None, None

# Fase 1: Ejecución
ruta_dataset = "cursos.csv"  
dataset = cargar_datos(ruta_dataset)

if dataset is not None:
    dataset = limpiar_datos(dataset)
    if dataset is not None:
        matriz_caracteristicas, vectorizador = generar_matriz_caracteristicas(dataset)
        if matriz_caracteristicas is not None:
            # Guardar la matriz generada en formato .npz
            scipy.sparse.save_npz("matriz_caracteristicas.npz", matriz_caracteristicas)
            print("Fase 1 completada: Procesamiento de datos terminado y matriz guardada.")
        else:
            print("Error en la generación de la matriz de características.")
    else:
        print("Error en el procesamiento de datos.")
else:
    print("Error al cargar los datos.")
