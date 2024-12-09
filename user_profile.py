import numpy as np
import scipy.sparse

# def cargar_matriz(ruta):
#     """
#     Carga la matriz TF-IDF desde un archivo.
#     """
#     try:
#         matriz = scipy.sparse.load_npz(ruta)
#         print(f"✔️ Matriz cargada desde: {ruta}")
#         return matriz
#     except FileNotFoundError:
#         print(f"❌ Error: No se encontró el archivo: {ruta}")
#         return None

def crear_perfil_usuario(interacciones, matriz):
    """
    Crea un perfil del usuario basado en interacciones.
    """
    num_cursos = matriz.shape[0]
    interacciones_validas = [i for i in interacciones if i < num_cursos]
    if not interacciones_validas:
        print("⚠️ No hay interacciones válidas para generar un perfil.")
        return np.zeros(matriz.shape[1])
    perfil_usuario = matriz[interacciones_validas].mean(axis=0)
    print("✔️ Perfil del usuario generado exitosamente.")
    return perfil_usuario

# # Ejecución
# if __name__ == "__main__":
#     ruta_matriz = "matriz_caracteristicas.npz"
#     matriz = cargar_matriz(ruta_matriz)
#     if matriz is not None:
#         interacciones_usuario = [1, 2, 5]
#         perfil_usuario = crear_perfil_usuario(interacciones_usuario, matriz)
#         print("Perfil del usuario:", perfil_usuario)
