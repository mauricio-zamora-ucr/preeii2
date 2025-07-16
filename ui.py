import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import platform
import random
import time

class ExpedientesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Expedientes")
        self.root.geometry("800x600")
        
        # Configuración según el sistema operativo
        self.setup_paths()
        
        # Variables para el grid y estadísticas
        self.tree = None
        self.total_registros_var = tk.StringVar()
        self.tiempo_total_var = tk.StringVar()
        
        # Crear widgets de la ventana principal
        self.create_main_widgets()
    
    def setup_paths(self):
        """Configura las rutas según el sistema operativo"""
        sistema = platform.system()
        if sistema == "Windows":
            self.default_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        elif sistema == "Darwin":  # Mac
            self.default_path = os.path.join(os.path.expanduser('~'), 'Desktop')
        else:  # Linux/Unix
            self.default_path = os.path.join(os.path.expanduser('~'), 'Escritorio')
        
        self.current_path = self.default_path
    
    def create_main_widgets(self):
        """Crea los widgets de la ventana principal"""
        # Marco principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill=tk.BOTH)
        
        # Título
        tk.Label(main_frame, text="Gestión de Expedientes", font=("Arial", 16, "bold")).pack(pady=10)
        
        # Botones
        btn_descargar = tk.Button(
            main_frame, 
            text="Descargar expedientes", 
            command=self.open_download_window,
            width=30,
            height=2
        )
        btn_descargar.pack(pady=10)
        
        btn_info = tk.Button(
            main_frame, 
            text="Ver Información", 
            command=self.show_info,
            width=30,
            height=2
        )
        btn_info.pack(pady=10)
        
        btn_generar = tk.Button(
            main_frame, 
            text="Generar expediente de datos en la RAM", 
            command=self.open_generate_window,
            width=30,
            height=2
        )
        btn_generar.pack(pady=10)
    
    def open_download_window(self):
        """Abre la ventana de descarga de expedientes"""
        self.download_window = tk.Toplevel(self.root)
        self.download_window.title("Descargar Expedientes")
        self.download_window.geometry("900x700")
        
        # Marco principal
        frame = tk.Frame(self.download_window, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Sección de ruta
        path_frame = tk.Frame(frame)
        path_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(path_frame, text="Ruta de guardado:").pack(anchor=tk.W)
        
        path_entry_frame = tk.Frame(path_frame)
        path_entry_frame.pack(fill=tk.X, pady=5)
        
        self.path_var = tk.StringVar(value=self.default_path)
        entry_path = tk.Entry(path_entry_frame, textvariable=self.path_var, width=60)
        entry_path.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        btn_browse = tk.Button(
            path_entry_frame, 
            text="Examinar", 
            command=self.browse_folder
        )
        btn_browse.pack(side=tk.LEFT, padx=5)
        
        # Sección del Treeview (grid)
        tree_frame = tk.Frame(frame)
        tree_frame.pack(expand=True, fill=tk.BOTH, pady=10)
        
        # Crear el Treeview con scrollbars
        scroll_y = tk.Scrollbar(tree_frame)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        
        scroll_x = tk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("carne", "nombre", "tiempo"),
            yscrollcommand=scroll_y.set,
            xscrollcommand=scroll_x.set,
            selectmode="extended"
        )
        
        self.tree.pack(expand=True, fill=tk.BOTH)
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Configurar columnas
        self.tree.heading("#0", text="#")
        self.tree.column("#0", width=50, stretch=tk.NO)
        
        self.tree.heading("carne", text="Carné")
        self.tree.column("carne", width=150, anchor=tk.CENTER)
        
        self.tree.heading("nombre", text="Nombre")
        self.tree.column("nombre", width=300, anchor=tk.W)
        
        self.tree.heading("tiempo", text="Tiempo (s)")
        self.tree.column("tiempo", width=100, anchor=tk.CENTER)
        
        # Sección de estadísticas
        stats_frame = tk.Frame(frame)
        stats_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(stats_frame, text="Total registros:").grid(row=0, column=0, padx=5, sticky=tk.E)
        tk.Entry(stats_frame, textvariable=self.total_registros_var, width=10, state='readonly').grid(row=0, column=1, padx=5, sticky=tk.W)
        
        tk.Label(stats_frame, text="Tiempo total:").grid(row=0, column=2, padx=5, sticky=tk.E)
        tk.Entry(stats_frame, textvariable=self.tiempo_total_var, width=10, state='readonly').grid(row=0, column=3, padx=5, sticky=tk.W)
        
        # Botones de acción
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, 
            text="Procesar", 
            command=self.process_download,
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame, 
            text="Reiniciar", 
            command=self.reset_download,
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame, 
            text="Salir", 
            command=self.download_window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=10)
    
    def browse_folder(self):
        """Abre el diálogo para seleccionar carpeta"""
        folder = filedialog.askdirectory(initialdir=self.default_path)
        if folder:
            self.path_var.set(folder)
            self.current_path = folder
    
    def process_download(self):
        """Procesa la descarga de expedientes (simulado)"""
        if not self.tree:
            return
        
        # Limpiar el treeview (excepto los headers)
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Generar datos de prueba
        nombres = ["Ana Pérez", "Carlos Rojas", "María González", "José Martínez", 
                  "Luisa Fernández", "Pedro Sánchez", "Laura Díaz", "Miguel López"]
        
        total_registros = random.randint(5, 15)
        tiempo_total = 0
        
        for i in range(1, total_registros + 1):
            carne = f"B{random.randint(10000, 99999)}"
            nombre = random.choice(nombres)
            tiempo = round(random.uniform(0.1, 2.5), 2)
            tiempo_total += tiempo
            
            self.tree.insert("", tk.END, text=str(i), values=(carne, nombre, tiempo))
        
        # Actualizar estadísticas
        self.total_registros_var.set(str(total_registros))
        self.tiempo_total_var.set(f"{tiempo_total:.2f}")
        
        messagebox.showinfo(
            "Proceso completado", 
            f"Se han descargado {total_registros} expedientes en:\n{self.path_var.get()}"
        )
    
    def reset_download(self):
        """Reinicia el formulario de descarga"""
        if self.tree:
            for item in self.tree.get_children():
                self.tree.delete(item)
        
        self.path_var.set(self.default_path)
        self.current_path = self.default_path
        self.total_registros_var.set("")
        self.tiempo_total_var.set("")
    
    def show_info(self):
        """Muestra la ventana de información"""
        info_window = tk.Toplevel(self.root)
        info_window.title("Información")
        info_window.geometry("600x400")
        
        # Marco con desplazamiento
        frame = tk.Frame(info_window)
        frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)
        
        # Texto de información
        info_text = """ESTA ES UNA VERSIÓN DE PRUEBA
EN CADA PREMATRICULA ALGO SE AGREGA O CORRIEGE        

ESTE SOFTWARE ES DE TIPO "AS IS"
https://en.wikipedia.org/wiki/As_is

Este script fue hecho en mi tiempo libre,
si quieren invitar a un combo de BK por
semestre que lo usen se les agradece.

            por Mauricio Zamora
             mauricio@zamora.cr"""
        
        # Mostrar texto centrado
        for line in info_text.split('\n'):
            tk.Label(frame, text=line, font=("Arial", 10)).pack()
        
        # Botón de salida
        tk.Button(
            info_window, 
            text="Cerrar", 
            command=info_window.destroy,
            width=15
        ).pack(pady=20)
    
    def open_generate_window(self):
        """Abre la ventana para generar expedientes en RAM"""
        generate_window = tk.Toplevel(self.root)
        generate_window.title("Generar Expediente en RAM")
        generate_window.geometry("400x200")
        
        # Marco principal
        frame = tk.Frame(generate_window, padx=20, pady=20)
        frame.pack(expand=True, fill=tk.BOTH)
        
        # Texto explicativo
        tk.Label(
            frame, 
            text="Generar expediente de datos en la RAM", 
            font=("Arial", 12)
        ).pack(pady=20)
        
        # Botones de acción
        btn_frame = tk.Frame(frame)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, 
            text="Generar", 
            command=self.generate_in_ram,
            width=15
        ).pack(side=tk.LEFT, padx=10)
        
        tk.Button(
            btn_frame, 
            text="Salir", 
            command=generate_window.destroy,
            width=15
        ).pack(side=tk.LEFT, padx=10)
    
    def generate_in_ram(self):
        """Simula la generación en RAM"""
        messagebox.showinfo(
            "Generar", 
            "Generando expediente en RAM\n\n(Función simulada)"
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpedientesApp(root)
    root.mainloop()