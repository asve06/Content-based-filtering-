import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import load_npz

# Cargar la matriz TF-IDF previamente generada
ruta_matriz = "matriz_caracteristicas.npz"
matriz_caracteristicas = load_npz(ruta_matriz)

# Cargar el perfil del usuario (simulando las interacciones)
from user_profile import crear_perfil_usuario

# Simulación de interacciones del usuario
interacciones_usuario = [1, 2, 5]  # Índices de los cursos favoritos del usuario
perfil_usuario = crear_perfil_usuario(interacciones_usuario, matriz_caracteristicas)

if perfil_usuario is None or np.all(perfil_usuario == 0):
    print("Error: No se pudo crear un perfil de usuario válido.")
else:
    def recomendar_cursos(perfil_usuario, matriz, top_n=5):
        """ 
        Genera recomendaciones basadas en similitud de coseno.
        :param perfil_usuario: Vector de características del usuario
        :param matriz: Matriz TF-IDF de los cursos
        :param top_n: Número de recomendaciones a devolver
        :return: Lista de índices de cursos recomendados y sus similitudes
        """
        # Verificar que el perfil del usuario tenga 2 dimensiones
        if perfil_usuario.ndim == 1:  # Si es un vector 1D, conviértelo a 2D
            perfil_usuario = perfil_usuario.reshape(1, -1)
        elif perfil_usuario.ndim > 2:  # Si es mayor a 2D, genera un error
            raise ValueError("El perfil del usuario tiene dimensiones incorrectas.")
        
        # Convertir perfil_usuario a un arreglo de numpy para evitar errores con np.matrix
        perfil_usuario = np.asarray(perfil_usuario)

        # Calcular similitudes de coseno
        similitudes = cosine_similarity(perfil_usuario, matriz).flatten()

        # Ordenar índices por similitud de mayor a menor
        indices_recomendados = np.argsort(similitudes)[::-1][:top_n]
        similitudes_recomendadas = similitudes[indices_recomendados]

        return indices_recomendados, similitudes_recomendadas

    # Generar las recomendaciones
    indices_recomendados, similitudes_recomendadas = recomendar_cursos(perfil_usuario, matriz_caracteristicas, top_n=5)

    # Mostrar resultados
    from info import cargar_datos  # Para cargar los datos originales y obtener nombres de los cursos

    ruta_dataset = "cursos.csv"  # Ruta del dataset original
    dataset = cargar_datos(ruta_dataset)

    if dataset is not None:
        print("\nRecomendaciones para el usuario:")
        for i, indice in enumerate(indices_recomendados):
            if indice < len(dataset):
                curso = dataset.iloc[indice]
                print(f"{i + 1}. {curso['nombre']} (Similitud: {similitudes_recomendadas[i]:.2f})")
    else:
        print("No se pudieron cargar los datos originales para mostrar los nombres de los cursos.")
