import numpy as np

def crear_perfil_usuario(usuario, matriz):
    """
    Crea un perfil del usuario basado en interacciones.
    """
    num_cursos = matriz.shape[0]
    cursos_vistos = usuario.get("cursos_vistos", [])
    cursos_interesados = usuario.get("interesados", [])
    cursos_no_interesados = usuario.get("no_interesados", [])
    
    perfil_usuario = np.zeros(matriz.shape[1])  # Iniciamos el perfil con un vector vacío

    for curso_id in cursos_interesados:
        if curso_id < matriz.shape[0]:
            perfil_usuario += matriz[curso_id].toarray().flatten() * 2  # Doble peso para cursos interesados
    for curso_id in cursos_no_interesados:
        if curso_id < matriz.shape[0]:
            perfil_usuario -= matriz[curso_id].toarray().flatten() * 2  # Menos peso para cursos no interesados

    # Ahora, agregamos los cursos vistos al perfil, pero con peso normal
    for curso_id in cursos_vistos:
        if curso_id < matriz.shape[0]:
            perfil_usuario += matriz[curso_id].toarray().flatten()

    print("✔️ Perfil del usuario generado exitosamente.")
    return perfil_usuario