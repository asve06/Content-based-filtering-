import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from info import cargar_datos, generar_matriz_caracteristicas
from user_profile import crear_perfil_usuario
from feedback import recopilar_feedback
from evaluation import evaluar_recomendaciones

RUTA_DATASET = "data/data.csv"
dataset = cargar_datos(RUTA_DATASET)

# Cargar la matriz de características (TF-IDF) y el vectorizador
matriz_caracteristicas, _ = generar_matriz_caracteristicas(dataset)

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

    if dataset is not None:
        print("\nRecomendaciones para el usuario:")
        for i, indice in enumerate(indices_recomendados):
            if indice < len(dataset):
                curso = dataset.iloc[indice]
                print(f"{i + 1}. {curso['nombre']} (Similitud: {similitudes_recomendadas[i]:.2f})")
        
        # Recopilar feedback del usuario
        recomendaciones = dataset.iloc[indices_recomendados]["nombre"].tolist()
        calificaciones = [4, 5, 3, 2, 5]  # Ejemplo de calificaciones proporcionadas por el usuario

        recopilar_feedback(usuario_id=1, recomendaciones=recomendaciones, calificaciones=calificaciones)

        # Evaluar las recomendaciones (suponiendo que reales es lo que el usuario realmente preferiría)
        reales = interacciones_usuario  # Cursos que realmente le gustan al usuario
        evaluar_recomendaciones(reales, indices_recomendados)
        
    else:
        print("No se pudieron cargar los datos originales para mostrar los nombres de los cursos.")
