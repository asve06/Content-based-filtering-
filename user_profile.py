import numpy as np

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
