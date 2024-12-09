import tkinter as tk
from tkinter import messagebox
import csv
from recommender import recomendar_cursos
from ast import literal_eval

# Leer datos del archivo CSV
def cargar_cursos(archivo_csv):
    cursos = []
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            cursos.append({
                "id": int(row["id"]),
                "nombre": row["nombre"],
                "descripcion": row["descripcion"],
                "categoria": row["categoria"],
                "nivel": row["nivel"]
            })
    return cursos

def cargar_usuarios(archivo_csv):
    usuarios = []
    with open(archivo_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                # Limpiar y convertir las cadenas a listas
                cursos_vistos = literal_eval(row["cursos_vistos"].strip())
                interesados = literal_eval(row["interesados"].strip())
                no_interesados = literal_eval(row["no_interesados"].strip())
                
                usuarios.append({
                    "id": int(row["usuario_id"]),
                    "nombre": row["nombre"],
                    "cursos_vistos": cursos_vistos,
                    "interesados": interesados,
                    "no_interesados": no_interesados
                })
            except Exception as e:
                print(f"Error al procesar la fila: {row}, Error: {e}")
    return usuarios


class RecomendacionesApp:
    def __init__(self, master, cursos):
        self.master = master
        self.master.title("Sistema de Recomendaciones de Cursos")
        
        # Cargar datos
        self.cursos = cursos
        self.cliente_seleccionado = tk.StringVar(value="Selecciona un cliente")
        self.recomendaciones = []
        self.cursos_vistos = []
        self.interesados = []
        self.no_interesados = []

        # Frame principal
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=10, pady=10)

        # Menú desplegable para seleccionar cliente
        self.cliente_menu = tk.OptionMenu(
            self.frame, self.cliente_seleccionado, *[cliente["nombre"] for cliente in clientes], 
            command=self.cambiar_cliente
        )
        self.cliente_seleccionado.set("Selecciona un cliente")  # Establecer valor predeterminado
        self.cliente_menu.pack(pady=5)

        # Frame para mostrar las tarjetas de recomendaciones
        self.cursos_frame = tk.Frame(self.frame)
        self.cursos_frame.pack(pady=10)

    def cambiar_cliente(self, cliente_nombre):
        # Buscar cliente seleccionado
        cliente = next((c for c in clientes if c["nombre"] == cliente_nombre), None)
        if cliente:
            self.cliente_id = cliente["id"]
            self.cursos_vistos = cliente["cursos_vistos"]  # Reiniciar cursos vistos
            self.interesados = cliente["interesados"]  # Reiniciar intereses
            self.no_interesados = cliente["no_interesados"]  # Reiniciar descartes
            self.actualizar_recomendaciones(cliente)

    def actualizar_recomendaciones(self, cliente):
        # Obtener recomendaciones del cliente
        if hasattr(self, 'cliente_id'):
            print(f"Recomendaciones numero 1")
            lista_recomendaciones, similitudes = recomendar_cursos(cliente)
            self.recomendaciones = lista_recomendaciones
        else:
            self.recomendaciones = []

        # Limpiar las tarjetas existentes
        for widget in self.cursos_frame.winfo_children():
            widget.destroy()

        # Crear una tarjeta para cada recomendación
        for curso_id in self.recomendaciones:
            curso = next((c for c in self.cursos if c["id"] == curso_id), None)
            if curso:
                self.crear_tarjeta_curso(curso, cliente)

    def crear_tarjeta_curso(self, curso, cliente):
        # Crear tarjeta
        tarjeta = tk.Frame(self.cursos_frame, borderwidth=2, relief="groove", padx=10, pady=10)
        tarjeta.pack(side="top", fill="x", pady=5)

        # Mostrar información básica
        tk.Label(tarjeta, text=f"{curso['nombre']}", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(tarjeta, text=f"Categoría: {curso['categoria']} | Nivel: {curso['nivel']}", font=("Arial", 10)).pack(anchor="w")

        # Tooltip para descripción
        def mostrar_descripcion(event):
            tooltip = tk.Toplevel(self.master)
            tooltip.wm_overrideredirect(True)  # Quitar barra de título
            x, y = event.x_root + 10, event.y_root + 10
            tooltip.wm_geometry(f"+{x}+{y}")
            tk.Label(tooltip, text=curso["descripcion"], background="lightyellow", relief="solid", borderwidth=1).pack()
            event.widget.tooltip = tooltip

        def ocultar_descripcion(event):
            if hasattr(event.widget, "tooltip"):
                event.widget.tooltip.destroy()
                del event.widget.tooltip

        tarjeta.bind("<Enter>", mostrar_descripcion)
        tarjeta.bind("<Leave>", ocultar_descripcion)

        # Botones de acción
        acciones_frame = tk.Frame(tarjeta)
        acciones_frame.pack(anchor="e", pady=5)

        tk.Button(
            acciones_frame, text="Me interesa",
            command=lambda: self.marcar_interes(curso["id"], cliente)
        ).pack(side="left", padx=5)

        tk.Button(
            acciones_frame, text="No me interesa",
            command=lambda: self.marcar_no_interes(curso["id"], cliente)
        ).pack(side="left", padx=5)

    def marcar_interes(self, curso_id, cliente):
        if curso_id not in cliente["interesados"]:
            cliente["interesados"].append(curso_id)
            if curso_id in cliente["no_interesados"]:
                cliente["no_interesados"].remove(curso_id)
            print(cliente["interesados"])
            messagebox.showinfo("Interés", f"El curso con ID {curso_id} ha sido marcado como 'Me interesa'.")

    def marcar_no_interes(self, curso_id, cliente):
        if curso_id not in cliente["no_interesados"]:
            cliente["no_interesados"].append(curso_id)
            if curso_id in cliente["interesados"]:
                cliente["interesados"].remove(curso_id)
            messagebox.showinfo("Descartado", f"El curso con ID {curso_id} ha sido marcado como 'No me interesa'.")

RUTA_DATASET = "data/data.csv"
RUTA_INTERRACIONES = "data/interacciones_usuarios.csv"

cursos = cargar_cursos(RUTA_DATASET)
clientes = cargar_usuarios(RUTA_INTERRACIONES)

# Crear la ventana principal
root = tk.Tk()
app = RecomendacionesApp(root, cursos)
root.mainloop()
