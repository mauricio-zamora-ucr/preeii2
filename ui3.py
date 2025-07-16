import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import platform
from datetime import datetime

class MainWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("DESCARGADOR DE PREMATRICULAS")
        self.root.geometry("650x450")
        
        # Configuración del estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        self.style.configure('Header.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('TButton', font=('Arial', 10), padding=5)
        self.style.configure('Footer.TLabel', font=('Arial', 8))
        
        # Crear y empaquetar el frame principal
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        self.title_label = ttk.Label(
            self.main_frame, 
            text="DESCARGADOR DE PREMATRICULAS", 
            style='Header.TLabel'
        )
        self.title_label.pack(pady=20)
        
        # Frame para los botones
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=30)
        
        # Botón 1: Descargar expedientes
        self.download_btn = ttk.Button(
            self.buttons_frame, 
            text="Descargar expedientes", 
            command=self.open_download_window,
            width=30
        )
        self.download_btn.grid(row=0, column=0, padx=10, pady=10)
        
        # Botón 2: Generar expediente en RAM
        self.process_btn = ttk.Button(
            self.buttons_frame, 
            text="Generar expediente en RAM", 
            command=self.open_process_window,
            width=30
        )
        self.process_btn.grid(row=1, column=0, padx=10, pady=10)
        
        # Botón 3: Ver información
        self.info_btn = ttk.Button(
            self.buttons_frame, 
            text="Ver información", 
            command=self.open_info_window,
            width=30
        )
        self.info_btn.grid(row=2, column=0, padx=10, pady=10)
        
        # Pie de página
        current_year = datetime.now().year
        self.footer_label = ttk.Label(
            self.main_frame, 
            text=f"Todos los derechos reservados por Mauricio Zamora - v1.0 - {current_year}",
            style='Footer.TLabel'
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=10)
    
    def open_download_window(self):
        DownloadWindow(self.root)
    
    def open_process_window(self):
        ProcessWindow(self.root)
    
    def open_info_window(self):
        InfoWindow(self.root)


class DownloadWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Descargar expedientes")
        self.geometry("850x650")
        self.resizable(False, False)
        
        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()
        
        # Configurar el grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Frame principal con padding
        self.main_frame = ttk.Frame(self, padding=(20, 10))
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Título
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Descargar expedientes", 
            style='Header.TLabel'
        )
        self.title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Sección de ubicación
        self.location_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Ubicación de descarga",
            padding=(10, 5)
        )
        self.location_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=5)
        
        # Campo de ubicación
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(
            self.location_frame, 
            textvariable=self.location_var, 
            width=60
        )
        self.location_entry.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Botón de explorar
        self.browse_btn = ttk.Button(
            self.location_frame, 
            text="Explorar...", 
            command=self.browse_location,
            width=12
        )
        self.browse_btn.grid(row=0, column=1, padx=5, pady=5)
        
        # Frame para botones de ubicaciones especiales
        self.special_locations_frame = ttk.Frame(self.location_frame)
        self.special_locations_frame.grid(row=1, column=0, columnspan=2, pady=(5, 0), sticky="ew")
        
        # Botón de escritorio
        self.desktop_btn = ttk.Button(
            self.special_locations_frame, 
            text="Usar Escritorio", 
            command=lambda: self.set_special_location("desktop"),
            width=15
        )
        self.desktop_btn.pack(side=tk.LEFT, padx=5)
        
        # Botón de documentos
        self.documents_btn = ttk.Button(
            self.special_locations_frame, 
            text="Usar Mis Documentos", 
            command=lambda: self.set_special_location("documents"),
            width=15
        )
        self.documents_btn.pack(side=tk.LEFT, padx=5)
        
        # Sección de autenticación
        self.auth_frame = ttk.LabelFrame(
            self.main_frame, 
            text="Autenticación",
            padding=(10, 10))
        self.auth_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        
        # Campo de usuario
        self.user_label = ttk.Label(
            self.auth_frame, 
            text="Digite su correo UCR sin el @ucr.ac.cr:",
            wraplength=400
        )
        self.user_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        
        self.user_var = tk.StringVar()
        self.user_entry = ttk.Entry(
            self.auth_frame, 
            textvariable=self.user_var,
            width=40
        )
        self.user_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Campo de contraseña
        self.pass_label = ttk.Label(
            self.auth_frame, 
            text="Contraseña:"
        )
        self.pass_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        
        self.pass_var = tk.StringVar()
        self.pass_entry = ttk.Entry(
            self.auth_frame, 
            textvariable=self.pass_var, 
            show="*",
            width=40
        )
        self.pass_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        
        # Botón de procesar
        self.process_btn = ttk.Button(
            self.auth_frame, 
            text="Procesar descarga", 
            command=self.process_download
        )
        self.process_btn.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Treeview (grid)
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=10)
        
        # Configurar grid para el treeview
        self.tree_frame.grid_columnconfigure(0, weight=1)
        self.tree_frame.grid_rowconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(
            self.tree_frame, 
            columns=("carne", "nombre", "tiempo"), 
            show="headings",
            height=10
        )
        
        self.tree.heading("carne", text="Carné")
        self.tree.heading("nombre", text="Nombre completo")
        self.tree.heading("tiempo", text="Tiempo estimado")
        
        self.tree.column("carne", width=120, anchor="center")
        self.tree.column("nombre", width=400, anchor="w")
        self.tree.column("tiempo", width=150, anchor="center")
        
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.tree_frame, 
            orient=tk.VERTICAL, 
            command=self.tree.yview
        )
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        # Totales
        self.totals_frame = ttk.Frame(self.main_frame)
        self.totals_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=5)
        
        self.total_records_var = tk.StringVar(value="Total expedientes: 0")
        self.total_records_label = ttk.Label(
            self.totals_frame, 
            textvariable=self.total_records_var
        )
        self.total_records_label.pack(side=tk.LEFT, padx=5)
        
        self.total_time_var = tk.StringVar(value="Tiempo total estimado: 0:00:00")
        self.total_time_label = ttk.Label(
            self.totals_frame, 
            textvariable=self.total_time_var
        )
        self.total_time_label.pack(side=tk.RIGHT, padx=5)
        
        # Botón de salir
        self.exit_btn = ttk.Button(
            self.main_frame, 
            text="Salir", 
            command=self.destroy,
            width=15
        )
        self.exit_btn.grid(row=5, column=2, pady=10, sticky="e")
        
        # Datos de prueba (simulados)
        self.load_sample_data()
    
    def browse_location(self):
        """Abre el diálogo para seleccionar directorio"""
        directory = filedialog.askdirectory()
        if directory:
            self.location_var.set(directory)
    
    def set_special_location(self, location_type):
        """Establece la ubicación especial (Escritorio o Documentos)"""
        system = platform.system()
        
        if system == "Windows":
            if location_type == "desktop":
                path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            else:  # documents
                path = os.path.join(os.environ['USERPROFILE'], 'Documents')
        elif system == "Darwin":  # Mac
            if location_type == "desktop":
                path = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:  # documents
                path = os.path.join(os.path.expanduser('~'), 'Documents')
        else:  # Linux y otros
            if location_type == "desktop":
                path = os.path.join(os.path.expanduser('~'), 'Desktop')
            else:  # documents
                path = os.path.join(os.path.expanduser('~'), 'Documents')
        
        self.location_var.set(path)
    
    def process_download(self):
        """Procesa la descarga"""
        if not self.user_var.get() or not self.pass_var.get() or not self.location_var.get():
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return
        
        # Aquí iría la lógica real de descarga
        messagebox.showinfo("Info", "Descarga procesada (simulación)")
    
    def clear_grid(self):
        """Limpia el grid"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        self.total_records_var.set("Total expedientes: 0")
        self.total_time_var.set("Tiempo total estimado: 0:00:00")
    
    def load_grid(self, data_list):
        """Carga datos en el grid
        
        Args:
            data_list (list): Lista de diccionarios con las claves:
                              'carne', 'nombre', 'tiempo'
        """
        self.clear_grid()
        
        total_time = 0
        for data in data_list:
            self.tree.insert("", tk.END, values=(
                data['carne'], 
                data['nombre'], 
                data['tiempo']
            ))
            
            # Sumar tiempo (asumiendo formato HH:MM:SS)
            h, m, s = map(int, data['tiempo'].split(':'))
            total_time += h * 3600 + m * 60 + s
        
        # Actualizar totales
        self.total_records_var.set(f"Total expedientes: {len(data_list)}")
        
        # Formatear tiempo total
        hours, remainder = divmod(total_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        self.total_time_var.set(
            f"Tiempo total estimado: {hours}:{minutes:02d}:{seconds:02d}"
        )
    
    def load_sample_data(self):
        """Carga datos de ejemplo"""
        sample_data = [
            {'carne': 'B12345', 'nombre': 'Juan Pérez Pérez', 'tiempo': '0:01:30'},
            {'carne': 'B54321', 'nombre': 'María Gómez Gómez', 'tiempo': '0:02:15'},
            {'carne': 'B98765', 'nombre': 'Carlos López López', 'tiempo': '0:01:45'},
            {'carne': 'B56789', 'nombre': 'Ana Rodríguez Rodríguez', 'tiempo': '0:03:20'},
            {'carne': 'B13579', 'nombre': 'Pedro Sánchez Sánchez', 'tiempo': '0:02:00'},
        ]
        self.load_grid(sample_data)


class ProcessWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Procesa expediente copiado en memoria")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()
        
        # Frame principal con padding
        self.main_frame = ttk.Frame(self, padding=(20, 15))
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Procesar expediente en memoria", 
            style='Header.TLabel'
        )
        self.title_label.pack(pady=(0, 15))
        
        # Área de resultados con scrollbar
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            self.text_frame, 
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            padx=10,
            pady=10,
            font=('Arial', 10)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.result_text.yview)
        
        # Frame para botones
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=15)
        
        # Botón de procesar
        self.process_btn = ttk.Button(
            self.buttons_frame, 
            text="Procesar", 
            command=self.process_data,
            width=15
        )
        self.process_btn.pack(side=tk.LEFT, padx=10)
        
        # Botón de salir
        self.exit_btn = ttk.Button(
            self.buttons_frame, 
            text="Salir", 
            command=self.destroy,
            width=15
        )
        self.exit_btn.pack(side=tk.LEFT, padx=10)
    
    def process_data(self):
        """Procesa los datos (simulado)"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        result = f"[{timestamp}] Expediente procesado en memoria\n"
        self.result_text.insert(tk.END, result)
        self.result_text.see(tk.END)
    
    def clear_results(self):
        """Limpia los resultados"""
        self.result_text.delete(1.0, tk.END)


class InfoWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Información")
        self.geometry("700x350")
        self.resizable(False, False)
        
        # Hacer la ventana modal
        self.transient(parent)
        self.grab_set()
        
        # Frame principal con padding
        self.main_frame = ttk.Frame(self, padding=(25, 15))
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        self.title_label = ttk.Label(
            self.main_frame, 
            text="Información", 
            style='Header.TLabel'
        )
        self.title_label.pack(pady=(0, 15))
        
        # Frame para el texto con scrollbar
        self.text_frame = ttk.Frame(self.main_frame)
        self.text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.info_text = tk.Text(
            self.text_frame, 
            wrap=tk.WORD,
            yscrollcommand=self.scrollbar.set,
            padx=10,
            pady=10,
            font=('Arial', 10),
            height=10
        )
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        self.scrollbar.config(command=self.info_text.yview)
        
        # Insertar texto
        info_content = """ESTA ES UNA VERSIÓN DE PRUEBA. EN CADA PREMATRÍCULA SE AGREGA O ACTUALIZA UNA FUNCIONALIDAD.

ESTE SOFTWARE ES DE TIPO "AS IS" (https://en.wikipedia.org/wiki/As_is)

Este script fue hecho en mi tiempo libre. Si quieren invitar a un combo de BK por semestre que lo usen, se les agradece.

Por Mauricio Zamora"""
        
        self.info_text.insert(tk.END, info_content)
        self.info_text.config(state=tk.DISABLED)  # Hacerlo de solo lectura
        
        # Botón de salir
        self.exit_btn = ttk.Button(
            self.main_frame, 
            text="Salir", 
            command=self.destroy,
            width=15
        )
        self.exit_btn.pack(pady=15)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainWindow(root)
    root.mainloop()