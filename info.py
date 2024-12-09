import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
    
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