import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import re

class TaskManagerLite:
    def __init__(self, root):
        self.root = root
        self.root.title("👑 Administrador de Tareas Lite - Control Total")
        self.root.geometry("650x450")
        
        # Estilo oscuro/profesional
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        # Contenedor principal
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tabla de procesos
        self.tree = ttk.Treeview(self.main_frame, columns=("Nombre", "PID", "Memoria"), show="headings")
        self.tree.heading("Nombre", text="Nombre del Proceso")
        self.tree.heading("PID", text="PID")
        self.tree.heading("Memoria", text="Uso de Memoria")
        
        self.tree.column("Nombre", width=250)
        self.tree.column("PID", width=100, anchor=tk.CENTER)
        self.tree.column("Memoria", width=150, anchor=tk.E)
        
        # Barra de desplazamiento
        self.scrollbar = ttk.Scrollbar(self.main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=self.scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Panel de botones
        self.btn_frame = ttk.Frame(root, padding="5")
        self.btn_frame.pack(fill=tk.X)
        
        self.btn_refresh = ttk.Button(self.btn_frame, text="🔄 Actualizar", command=self.actualizar_procesos)
        self.btn_refresh.pack(side=tk.LEFT, padx=5)
        
        self.btn_kill = ttk.Button(self.btn_frame, text="🛑 Finalizar Tarea", command=self.matar_proceso)
        self.btn_kill.pack(side=tk.RIGHT, padx=5)
        
        # Carga inicial
        self.actualizar_procesos()

    def actualizar_procesos(self):
        # Limpiar tabla
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        try:
            # Obtener procesos de Windows sin privilegios elevados
            out = subprocess.check_output("tasklist /NH /FO CSV", shell=True).decode('cp1252')
            lineas = out.strip().split('\n')
            
            for linea in lineas:
                if not linea.strip(): continue
                # Parsear formato CSV nativo ("nombre","pid","sesion","num_sesion","memoria")
                partes = [p.strip('"') for p in linea.split('","')]
                if len(partes) >= 5:
                    nombre = partes[0]
                    pid = partes[1]
                    memoria = partes[4]
                    self.tree.insert("", tk.END, values=(nombre, pid, memoria))
        except Exception as e:
            messagebox.onerror("Error", f"No se pudieron leer los procesos: {e}")

    def matar_proceso(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un proceso de la lista.")
            return
            
        valores = self.tree.item(selected_item, "values")
        nombre = valores[0]
        pid = valores[1]
        
        respuesta = messagebox.askyesno("Confirmar", f"¿Seguro que deseas forzar el cierre de {nombre} (PID: {pid})?")
        if respuesta:
            try:
                # Intento de finalización en espacio de usuario
                subprocess.check_output(f"taskkill /F /PID {pid}", shell=True)
                messagebox.showinfo("Éxito", f"Proceso {pid} finalizado.")
                self.root.after(500, self.actualizar_procesos)
            except Exception:
                messagebox.showerror("Acceso Denegado", f"No puedes cerrar {nombre}. Es un proceso del Sistema Protegido.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerLite(root)
    root.mainloop()
