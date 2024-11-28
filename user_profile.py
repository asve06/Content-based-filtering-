import numpy as np
import scipy.sparse

# Cargar la matriz TF-IDF generada previamente
ruta_guardado = "matriz_caracteristicas.npz"
matriz_caracteristicas = scipy.sparse.load_npz(ruta_guardado)

# Función para crear el perfil del usuario
def crear_perfil_usuario(interacciones, matriz):
    """
    Crea un perfil de usuario basado en los cursos con los que ha interactuado.
    :param interacciones: Lista de índices de los cursos que el usuario ha marcado como favoritos
    :param matriz: Matriz TF-IDF de los cursos
    :return: Vector de perfil del usuario
    """
    # Verificar que los índices estén dentro de los límites de la matriz
    num_cursos = matriz.shape[0]  # Número de cursos en la matriz
    interacciones_validas = [i for i in interacciones if i < num_cursos]

    if not interacciones_validas:  # Si no hay interacciones válidas
        print("No hay interacciones válidas.")
        return np.zeros(matriz.shape[1])  # Devuelve un vector vacío
    
    # Calcula el promedio de las características de los cursos seleccionados
    perfil_usuario = matriz[interacciones_validas].mean(axis=0)
    return perfil_usuario

# Simulación de interacciones del usuario
# Supongamos que el usuario ha interactuado con los cursos en los índices 0, 2 y 5
interacciones_usuario = [1, 2, 5]

# Crear el perfil del usuario
perfil_usuario = crear_perfil_usuario(interacciones_usuario, matriz_caracteristicas)

# Imprimir el perfil del usuario (vector de características)
print("Fase 2 completada: Perfil del usuario creado.")
print("Perfil del usuario:", perfil_usuario)
