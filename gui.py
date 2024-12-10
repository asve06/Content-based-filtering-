import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
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

        # Botón de refrescar
        self.boton_refresh = tk.Button(self.frame, text="Refresh", command=self.refresh)
        self.boton_refresh.pack(pady=5)

        # Crear el Notebook (pestañas)
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(pady=10)
        
        # Pestaña Principal con Scrollbar
        self.pestana_principal_container = tk.Frame(self.notebook)  # Contenedor general
        self.notebook.add(self.pestana_principal_container, text="Principal")

        # Crear un canvas para permitir desplazamiento
        self.canvas_principal = tk.Canvas(self.pestana_principal_container)
        self.scrollbar_principal = tk.Scrollbar(
            self.pestana_principal_container, orient="vertical", command=self.canvas_principal.yview
        )
        self.canvas_principal.configure(yscrollcommand=self.scrollbar_principal.set)

        # Empaquetar canvas y scrollbar
        self.canvas_principal.pack(side="left", fill="both", expand=True)
        self.scrollbar_principal.pack(side="right", fill="y")

        # Frame interno para widgets
        self.pestana_principal = tk.Frame(self.canvas_principal)
        self.canvas_principal.create_window((0, 0), window=self.pestana_principal, anchor="nw")

        # Configurar el evento para ajustar el scroll cuando cambie el contenido
        self.pestana_principal.bind("<Configure>", self.actualizar_scroll)

    
        # Pestaña Recomendado
        self.pestana_recomendados = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_recomendados, text="Recomendado")

        # Pestaña Vistos
        self.pestana_vistos = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_vistos, text="Vistos")

        # Pestaña Interesados
        self.pestana_interesados = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_interesados, text="Interesados")

        # Pestaña No Interesados
        self.pestana_no_interesados = tk.Frame(self.notebook)
        self.notebook.add(self.pestana_no_interesados, text="No Interesados")

    # Método para ajustar el tamaño del canvas
    def actualizar_scroll(self, event=None):
        self.canvas_principal.configure(scrollregion=self.canvas_principal.bbox("all"))
        
    def refresh(self):
        # Actualiza las recomendaciones y los cursos vistos, interesados y no interesados
        cliente_nombre = self.cliente_seleccionado.get()
        if cliente_nombre != "Selecciona un cliente":
            cliente = next((c for c in clientes if c["nombre"] == cliente_nombre), None)
            if cliente:
                self.cursos_vistos = cliente["cursos_vistos"]
                self.interesados = cliente["interesados"]
                self.no_interesados = cliente["no_interesados"]
                self.actualizar_recomendaciones(cliente)
                self.actualizar_pestana_principal()

    def cambiar_cliente(self, cliente_nombre):
        # Buscar cliente seleccionado
        cliente = next((c for c in clientes if c["nombre"] == cliente_nombre), None)
        if cliente:
            self.cliente_id = cliente["id"]
            self.cursos_vistos = cliente["cursos_vistos"]  # Reiniciar cursos vistos
            self.interesados = cliente["interesados"]  # Reiniciar intereses
            self.no_interesados = cliente["no_interesados"]  # Reiniciar descartes
            self.actualizar_recomendaciones(cliente)

    def limpiar_pestanas(self):
        # Limpiar las pestañas
        for frame in [self.pestana_principal, self.pestana_vistos, self.pestana_interesados, 
                      self.pestana_no_interesados, self.pestana_recomendados]:
            for widget in frame.winfo_children():
                widget.destroy()

    def actualizar_pestana_vistos(self):
        for curso_id in self.cursos_vistos:
            curso = next((c for c in self.cursos if c["id"] == curso_id), None)
            if curso:
                self.crear_tarjeta_curso(curso, self.pestana_vistos, show_buttons=False)

    def actualizar_pestana_interesados(self):
        for curso_id in self.interesados:
            curso = next((c for c in self.cursos if c["id"] == curso_id), None)
            if curso:
                self.crear_tarjeta_curso(curso, self.pestana_interesados, show_buttons=False)

    def actualizar_pestana_no_interesados(self):
        for curso_id in self.no_interesados:
            curso = next((c for c in self.cursos if c["id"] == curso_id), None)
            if curso:
                self.crear_tarjeta_curso(curso, self.pestana_no_interesados, show_buttons=False)

    def actualizar_pestana_principal(self):
    # Limpiar los widgets existentes en la pestaña principal
        for widget in self.pestana_principal.winfo_children():
            widget.destroy()

        # Filtrar cursos excluyendo los interesados y no interesados
        cursos_filtrados = [
            curso for curso in self.cursos
            if curso["id"] not in self.interesados and curso["id"] not in self.no_interesados
        ]

        # Mostrar los cursos filtrados
        for i, curso in enumerate(cursos_filtrados):
            similitud = self.similitudes[i] if i < len(self.similitudes) else None
            self.crear_tarjeta_curso(curso, self.pestana_principal, show_buttons=True)
        
    def actualizar_pestana_recomendados(self):
        for i, curso_id in enumerate(self.recomendaciones):
            curso = next((c for c in self.cursos if c["id"] == curso_id), None)
            if curso:
                similitud = self.similitudes[i]  # Obtener la similitud correspondiente
                self.crear_tarjeta_curso(curso, self.pestana_recomendados, similitud)
                
    def actualizar_recomendaciones(self, cliente):
        # Obtener recomendaciones del cliente
        if hasattr(self, 'cliente_id'):
            lista_recomendaciones, similitudes = recomendar_cursos(cliente)
            self.recomendaciones = lista_recomendaciones
            self.similitudes = similitudes  # Guardamos las similitudes
        else:
            self.recomendaciones = []

        # Limpiar las pestañas
        self.limpiar_pestanas()

        # Actualizar la pestaña de Recomendados
        self.actualizar_pestana_recomendados()

        # Actualizar las demás pestañas
        self.actualizar_pestana_vistos()
        self.actualizar_pestana_interesados()
        self.actualizar_pestana_no_interesados()
        self.actualizar_pestana_principal()
        

    def crear_tarjeta_curso(self, curso, pestana, similitud=None, show_buttons=False):
        # Crear tarjeta
        tarjeta = tk.Frame(pestana, borderwidth=2, relief="groove", padx=10, pady=10)
        tarjeta.pack(side="top", fill="x", pady=5)

        # Mostrar información básica
        tk.Label(tarjeta, text=f"{curso['nombre']}", font=("Arial", 12, "bold")).pack(anchor="w")
        tk.Label(tarjeta, text=f"Categoría: {curso['categoria']} | Nivel: {curso['nivel']}", font=("Arial", 10)).pack(anchor="w")

        # Mostrar la similitud si se proporciona
        if similitud is not None:
            frame = tk.Frame(tarjeta)
            frame.pack(anchor="w", fill="x", padx=10)
            tk.Label(frame, text=f"{similitud*100:.2f}%", font=("Arial", 20, "bold italic"), fg="pink").pack(side="right")
            tk.Label(frame, text="Coincidencia:", font=("Arial", 14, "italic"), fg="pink").pack(side="right")
            if similitud >= 0.7:
                tk.Label(frame, text="¡Este es el curso para ti👐!", font=("Arial", 14, "bold"), fg="lightgreen").pack(anchor="w", padx=10)

        # Mostrar botones solo en la pestaña principal
        if pestana == self.pestana_principal and show_buttons:
            acciones_frame = tk.Frame(tarjeta)
            acciones_frame.pack(anchor="e", pady=5)

            # Botón "Me interesa"
            tk.Button(
                acciones_frame, text="Me interesa 👍",
                command=lambda: self.marcar_interes(curso["id"], self.cliente_seleccionado.get())
            ).pack(side="left", padx=5)

            # Botón "No me interesa"
            tk.Button(
                acciones_frame, text="No me interesa 👎",
                command=lambda: self.marcar_no_interes(curso["id"], self.cliente_seleccionado.get())
            ).pack(side="left", padx=5)
            
        # Tooltip para descripción
        def mostrar_descripcion(event):
            tooltip = tk.Toplevel(self.master)
            tooltip.wm_overrideredirect(True)  # Quitar barra de título
            x, y = event.x_root + 10, event.y_root + 10
            tooltip.wm_geometry(f"+{x}+{y}")
            tk.Label(tooltip, text=curso["descripcion"], background="lightyellow", relief="solid", borderwidth=1, fg="black").pack()
            tarjeta.tooltip = tooltip

        def ocultar_descripcion(event):
            if hasattr(tarjeta, "tooltip"):
                tarjeta.tooltip.destroy()
                del tarjeta.tooltip

        tarjeta.bind("<Enter>", mostrar_descripcion)
        tarjeta.bind("<Leave>", ocultar_descripcion)

    

    def marcar_interes(self, curso_id, cliente_nombre):
        cliente = next((c for c in clientes if c["nombre"] == cliente_nombre), None)
        if curso_id not in cliente["interesados"]:
            cliente["interesados"].append(curso_id)
            if curso_id in cliente["no_interesados"]:
                cliente["no_interesados"].remove(curso_id)
            messagebox.showinfo("Interés", f"El curso con ID {curso_id} ha sido marcado como 'Me interesa'.")

    def marcar_no_interes(self, curso_id, cliente_nombre):
        cliente = next((c for c in clientes if c["nombre"] == cliente_nombre), None)
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
