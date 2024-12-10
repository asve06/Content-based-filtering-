#calcula la precisión y recall comparando las listas de elementos reales y recomendadas, 
# mostrando los detalles como los verdaderos positivos, falsos positivos y falsos negativos, 
# y retorna las métricas calculadas.

def evaluar_recomendaciones(reales, recomendadas):
    """
    Evalúa las recomendaciones con precisión, recall, y muestra detalles de la evaluación.
    """
    reales_set, recomendadas_set = set(reales), set(recomendadas)
    
    # Cálculo de los verdaderos positivos, falsos positivos y falsos negativos
    verdaderos_positivos = len(reales_set & recomendadas_set)  # Elementos comunes
    falsos_positivos = len(recomendadas_set - reales_set)  # Elementos recomendados pero no reales
    falsos_negativos = len(reales_set - recomendadas_set)  # Elementos reales pero no recomendados

    # Cálculo de precisión y recall
    precision = verdaderos_positivos / len(recomendadas) if len(recomendadas) > 0 else 0
    recall = verdaderos_positivos / len(reales) if len(reales) > 0 else 0

    # Mostrar resultados detallados
    print("\n=== Evaluación de Recomendaciones ===")
    print(f"Total de elementos reales: {len(reales)}")
    print(f"Total de recomendaciones: {len(recomendadas)}")
    print(f"Verdaderos positivos: {verdaderos_positivos}")
    print(f"Falsos positivos: {falsos_positivos}")
    print(f"Falsos negativos: {falsos_negativos}")
    print(f"Precisión: {precision:.2f}")
    print(f"Recall: {recall:.2f}")

    return precision, recall
