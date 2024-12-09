# Diccionario global para almacenar el feedback
feedback = {}

def recopilar_feedback(usuario_id, recomendaciones, calificaciones):
    """
    Recopila retroalimentación del usuario para cada recomendación.
    """
    # Validar que las listas de recomendaciones y calificaciones tengan el mismo tamaño
    if len(recomendaciones) != len(calificaciones):
        print("❌ Error: Las recomendaciones y calificaciones no coinciden.")
        return
    
    # Validar que las calificaciones sean numéricas
    if not all(isinstance(cal, (int, float)) for cal in calificaciones):
        print("❌ Error: Todas las calificaciones deben ser numéricas.")
        return

    # Guardar el feedback en el diccionario global
    feedback[usuario_id] = {
        "recomendaciones": recomendaciones,
        "calificaciones": calificaciones,
    }

    # Mostrar el feedback guardado
    print("\n=== Feedback Guardado ===")
    for rec, cal in zip(recomendaciones, calificaciones):
        print(f"Recomendación: {rec} -> Calificación: {cal}")

# La función ahora solo hace la recopilación de feedback y muestra el resultado.
