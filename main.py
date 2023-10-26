import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime, timedelta

class TaskManagerApp:
    def __init__(self, root):
        self.root = root # Se inicia la aplicacion
        self.root.title("Gestión de Tareas")
        
        self.tasks = [] # Se inicializa la lista para guardar tareas
        
        # Creacion de los titulos y botones de la aplicacion
        self.title_label = tk.Label(root, text="Título:")
        self.title_entry = tk.Entry(root)
        
        self.start_label = tk.Label(root, text="Fecha de Inicio (DD-MM-YYYY HH:MM):")
        self.start_entry = tk.Entry(root)
        
        self.end_label = tk.Label(root, text="Fecha de Finalización (DD-MM-YYYY HH:MM):")
        self.end_entry = tk.Entry(root)
        
        self.description_label = tk.Label(root, text="Descripción:")
        self.description_entry = tk.Entry(root)
        
        self.subtask_label = tk.Label(root, text="Subtareas:")
        self.subtask_entry = tk.Entry(root)
        
        self.add_button = tk.Button(root, text="Agregar Tarea", command=self.add_task)
        self.edit_button = tk.Button(root, text="Editar Tarea", command=self.edit_task)
        self.delete_button = tk.Button(root, text="Eliminar Tarea", command=self.delete_task)
        self.complete_button = tk.Button(root, text="Completar campos", command=self.complete_fields)
        
        self.task_list = ttk.Treeview(root, columns=("Título", "Inicio", "Finalización", "Descripción", "Subtareas", "Tiempo Restante"))
        self.task_list.heading("#1", text="Título")
        self.task_list.heading("#2", text="Inicio")
        self.task_list.heading("#3", text="Finalización")
        self.task_list.heading("#4", text="Descripción")
        self.task_list.heading("#5", text="Subtareas")
        self.task_list.heading("#6", text="Tiempo Restante")
        
        self.task_list.column("#1", width=150)
        self.task_list.column("#2", width=150)
        self.task_list.column("#3", width=150)
        self.task_list.column("#4", width=200)
        self.task_list.column("#5", width=200)
        self.task_list.column("#6", width=150)
        
        self.task_list.pack(pady=10)
        
        self.title_label.pack()
        self.title_entry.pack(pady=5)
        self.start_label.pack()
        self.start_entry.pack(pady=5)
        self.end_label.pack()
        self.end_entry.pack(pady=5)
        self.description_label.pack()
        self.description_entry.pack(pady=5)
        self.subtask_label.pack()
        self.subtask_entry.pack(pady=5)
        self.add_button.pack(pady=7)
        self.edit_button.pack(pady=7)
        self.delete_button.pack(pady=7)
        self.complete_button.pack(pady=7)

        self.add_button.config(pady=3, padx=6, bg='#65C635', foreground='white')
        self.edit_button.config(pady=3, padx=6)
        self.delete_button.config(pady=3, padx=6, bg='#F1584B', foreground='white')
        self.complete_button.config(pady=3, padx=6)

    def add_task(self):
        # Variables de la informacion de las tareas
        title = self.title_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        description = self.description_entry.get()
        subtasks = self.subtask_entry.get()
        
        try:
            start_date = datetime.strptime(start, "%d-%m-%Y %H:%M")
            end_date = datetime.strptime(end, "%d-%m-%Y %H:%M")
            
            if end_date < start_date: # Se verifica si la fecha de finalizacion es menor a la de inicio
                messagebox.showerror("Error", "La fecha de finalización debe ser posterior a la fecha de inicio.")
                return
            
            time_remaining = end_date - start_date # Se calcula el tiempo restante entre las dos fechas
            
            self.tasks.append((title, start, end, description, subtasks, str(time_remaining))) # Se añade la tarea
            
            self.update_task_list() 
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use DD-MM-YYYY HH:MM.")
    
    def complete_fields(self):
        selected_item = self.task_list.selection() # Obtenemos la tarea seleccionada
        if not selected_item: # Si no se selecciono nada se le pedira al usuario que seleccione una tarea
            messagebox.showerror("Error", "Seleccione una tarea para rellenar los campos.")
            return
        
        try:
            info = self.task_list.item(selected_item[0]) # Informacion de la tarea
            dicObject = info.values()
            values = list(dicObject)
            
            title = values[2][0]
            start = values[2][1]
            end = values[2][2]
            description = values[2][3]
            subtasks = values[2][4]

            # Se añade la informacion a los campos vacios
            self.title_entry.insert(tk.END, title)
            self.start_entry.insert(tk.END, start)
            self.end_entry.insert(tk.END, end)
            self.description_entry.insert(tk.END, description)
            self.subtask_entry.insert(tk.END, subtasks)
        except ValueError:
            messagebox.showerror('Error', 'Ocurrio un error inesperado.')

    def edit_task(self):
        selected_item = self.task_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una tarea para editar.")
            return
        
        index = self.task_list.index(selected_item) # Obtiene la posicion de la tarea en la tabla
        
        title = self.title_entry.get()
        start = self.start_entry.get()
        end = self.end_entry.get()
        description = self.description_entry.get()
        subtasks = self.subtask_entry.get()
        
        try:
            start_date = datetime.strptime(start, "%d-%m-%Y %H:%M")
            end_date = datetime.strptime(end, "%d-%m-%Y %H:%M")
            
            if end_date < start_date:
                messagebox.showerror("Error", "La fecha de finalización debe ser posterior a la fecha de inicio.")
                return
            
            time_remaining = end_date - start_date
            
            self.tasks[index] = (title, start, end, description, subtasks, str(time_remaining))
            
            self.update_task_list()
            self.clear_entries()
        except ValueError:
            messagebox.showerror("Error", "Formato de fecha incorrecto. Use DD-MM-YYYY HH:MM.")
    
    def delete_task(self):
        selected_item = self.task_list.selection()
        if not selected_item:
            messagebox.showerror("Error", "Seleccione una tarea para eliminar.")
            return
        
        index = self.task_list.index(selected_item)
        del self.tasks[index]
        self.update_task_list()
        self.clear_entries()
    
    def update_task_list(self):
        for item in self.task_list.get_children():
            self.task_list.delete(item)
        
        for task in self.tasks:
            self.task_list.insert("", "end", values=task)
    
    def clear_entries(self):
        self.title_entry.delete(0, "end")
        self.start_entry.delete(0, "end")
        self.end_entry.delete(0, "end")
        self.description_entry.delete(0, "end")
        self.subtask_entry.delete(0, "end")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()