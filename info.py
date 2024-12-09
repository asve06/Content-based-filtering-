import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def cargar_datos(ruta):
    """
    Carga el dataset desde un archivo CSV.
    """
    try:
        df = pd.read_csv(ruta)
        print(f"✔️ Archivo cargado exitosamente desde: {ruta}")
        return df
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo en la ruta: {ruta}")
        return None

def limpiar_datos(df):
    """
    Limpia y procesa los datos del DataFrame.
    """
    if "descripcion" not in df.columns:
        print("❌ Error: Falta la columna 'descripcion' en los datos.")
        return None
    df["descripcion"] = df["descripcion"].fillna("").str.lower()
    print("✔️ Datos limpiados y listos para el análisis.")
    return df

def generar_matriz_caracteristicas(df):
    """
    Genera la matriz TF-IDF basada en las descripciones.
    """
    try:
        df = limpiar_datos(df)
        vectorizador = TfidfVectorizer(stop_words="english")
        matriz = vectorizador.fit_transform(df["descripcion"])
        print("✔️ Matriz TF-IDF generada exitosamente.")
        return matriz, vectorizador
    except Exception as e:
        print(f"❌ Error al generar la matriz TF-IDF: {e}")
        return None, None

# def guardar_matriz(matriz, ruta_guardado):
#     """
#     Guarda la matriz TF-IDF en un archivo.
#     """
#     try:
#         scipy.sparse.save_npz(ruta_guardado, matriz)
#         print(f"✔️ Matriz TF-IDF guardada en: {ruta_guardado}")
#     except Exception as e:
#         print(f"❌ Error al guardar la matriz: {e}")

# Ejecución
# if __name__ == "__main__":
#     ruta_dataset = "cursos.csv"
#     ruta_guardado_matriz = "matriz_caracteristicas.npz"
#     dataset = cargar_datos(ruta_dataset)
#     if dataset is not None:
#         dataset = limpiar_datos(dataset)
#         if dataset is not None:
#             matriz, _ = generar_matriz_caracteristicas(dataset)
#             if matriz is not None:
#                 guardar_matriz(matriz, ruta_guardado_matriz)
