import tkinter as tk
from tkinter import messagebox
from recommender import generar_recomendaciones_usuario
from user_profile import actualizar_perfil_usuario
from info import cargar_datos_usuario, guardar_interacciones_usuario

# # Ejemplo de la matriz de características de cursos (esto sería más complejo en una aplicación real)
# matriz_caracteristicas = [
#     [0.1, 0.3, 0.5],
#     [0.3, 0.6, 0.2],
#     [0.4, 0.5, 0.1],
#     [0.6, 0.2, 0.8],
#     [0.7, 0.5, 0.3]
# ]

# # Ejemplo de un dataset de cursos (esto puede provenir de un CSV o base de datos)
# dataset = [
#     {'nombre': 'Curso 1', 'descripcion': 'Curso básico de Python'},
#     {'nombre': 'Curso 2', 'descripcion': 'Curso intermedio de Java'},
#     {'nombre': 'Curso 3', 'descripcion': 'Curso avanzado de C++'},
#     {'nombre': 'Curso 4', 'descripcion': 'Curso de Inteligencia Artificial'},
#     {'nombre': 'Curso 5', 'descripcion': 'Curso de Machine Learning'}
# ]

class RecomendacionesApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Sistema de Recomendaciones de Cursos")
        
        self.usuario_id = 1  # Suponemos que el ID del usuario es 1
        self.recomendaciones = []
        
        # Frame principal
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)
        
        # Listbox para mostrar recomendaciones
        self.listbox = tk.Listbox(self.frame, width=50, height=10)
        self.listbox.pack(pady=5)
        
        # Botón para actualizar recomendaciones
        self.update_button = tk.Button(self.frame, text="Actualizar Recomendaciones", command=self.actualizar_recomendaciones)
        self.update_button.pack(pady=5)
        
        # Botón para marcar como favorito
        self.favorite_button = tk.Button(self.frame, text="Marcar como Favorito", command=self.marcar_como_favorito)
        self.favorite_button.pack(pady=5)
        
        # Mostrar recomendaciones iniciales
        self.actualizar_recomendaciones()

    def actualizar_recomendaciones(self):
        # Cargar datos del usuario
        cursos_vistos, favoritos = cargar_datos_usuario(self.usuario_id)
        
        # Generar nuevas recomendaciones
        self.recomendaciones = generar_recomendaciones_usuario(self.usuario_id, matriz_caracteristicas, dataset)
        
        # Limpiar la listbox
        self.listbox.delete(0, tk.END)
        
        # Agregar las recomendaciones a la listbox
        for recomendacion in self.recomendaciones:
            self.listbox.insert(tk.END, f"{recomendacion[0]} (Similitud: {recomendacion[1]:.2f})")
    
    def marcar_como_favorito(self):
        # Obtener el índice seleccionado de la listbox
        seleccion = self.listbox.curselection()
        
        if not seleccion:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un curso.")
            return
        
        curso_seleccionado = self.recomendaciones[seleccion[0]][0]  # Nombre del curso
        # Buscar el índice del curso en el dataset
        curso_id = next(i for i, curso in enumerate(dataset) if curso['nombre'] == curso_seleccionado)
        
        # Marcar el curso como favorito y actualizar recomendaciones
        actualizar_perfil_usuario(self.usuario_id, curso_id, es_favorito=True, matriz_caracteristicas=matriz_caracteristicas)
        
        messagebox.showinfo("Éxito", f"El curso '{curso_seleccionado}' ha sido marcado como favorito.")
        
        # Actualizar la lista de recomendaciones
        self.actualizar_recomendaciones()

# Crear la ventana principal
root = tk.Tk()
app = RecomendacionesApp(root)
root.mainloop()
