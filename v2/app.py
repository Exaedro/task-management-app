import tkinter as tk
from tkinter import simpledialog, messagebox
from tkcalendar import *
import threading

# Diccionario para almacenar las tareas
tareas = {}

def set_interval(func, sec):
    def func_wrapper():
        set_interval(func, sec)
        func()
    t = threading.Timer(sec, func_wrapper)
    t.setDaemon(True)
    t.start()
    return t

def agregar_tarea():
    fecha = seleccion_fecha.get()
    titulo = simpledialog.askstring("Título", "Ingrese el título de la tarea:")
    if not titulo:
        return

    descripcion = simpledialog.askstring("Descripción", "Ingrese una descripción de la tarea:")
    if not descripcion:
        return

    if fecha in tareas:
        tareas[fecha].append({"titulo": titulo, "descripcion": descripcion})
    else:
        tareas[fecha] = [{"titulo": titulo, "descripcion": descripcion}]

    actualizar_calendario()

def editar_tarea():
    fecha = seleccion_fecha.get()
    if not fecha in tareas: return messagebox.showinfo("Editar Tarea", "No hay tareas para editar en esta fecha.")

    tarea = tareas[fecha]
    tarea_str = ""
    for i, t in enumerate(tarea):
        tarea_str += f"{i + 1}. {t['titulo']}\n"

    if not tarea_str: return messagebox.showinfo("Editar Tarea", "No hay tareas para editar en esta fecha.")
    
    tarea_idx = simpledialog.askinteger("Editar Tarea", f"Seleccione la tarea a editar:\n{tarea_str}", minvalue=1, maxvalue=len(tareas))
    if not tarea_idx: return
    tarea_idx -= 1

    nuevo_titulo = simpledialog.askstring("Nuevo Título", "Ingrese el nuevo título de la tarea:")
    if not nuevo_titulo: return
    
    nuevo_descripcion = simpledialog.askstring("Nueva Descripción", "Ingrese la nueva descripción de la tarea:")
    if not nuevo_descripcion: return
    
    tarea[tarea_idx]['titulo'] = nuevo_titulo
    tarea[tarea_idx]['descripcion'] = nuevo_descripcion
    actualizar_calendario()
        
def borrar_tarea():
    fecha = seleccion_fecha.get()
    if not fecha in tareas: return messagebox.showinfo("Borrar Tarea", "No hay tareas para borrar en esta fecha.")

    tarea = tareas[fecha]
    tarea_str = ""
    for i, t in enumerate(tarea):
        tarea_str += f"{i + 1}. {t['titulo']}\n"

    if not tarea_str: return messagebox.showinfo("Borrar Tarea", "No hay tareas para borrar en esta fecha.")
    
    tarea_idx = simpledialog.askinteger("Borrar Tarea", f"Seleccione la tarea a borrar:\n{tarea_str}", minvalue=1, maxvalue=len(tarea))
    if not tarea_idx: return

    tarea_idx -= 1
    tarea.pop(tarea_idx)
    if not tarea:
        del tareas[fecha]
    actualizar_calendario()
 
def actualizar_calendario():
    fecha = seleccion_fecha.get()
    if not fecha in tareas:
        return tarea_label.config(text="No hay tareas para esta fecha.")
        
    tarea = tareas[fecha]
    tarea_str = ""
    for i, t in enumerate(tarea):
        tarea_str += f"{i + 1}. {t['titulo']}\n"
    tarea_label.config(text=tarea_str)
        
def establecer_fecha():
    valor = calendario.selection_get()
    if valor:
        seleccion_fecha.set(valor)
        actualizar_calendario()

# Crear la ventana principal
root = tk.Tk()
root.title("Calendario de Tareas")
root.config(bg='#333435')

# Crear un selector de fecha
seleccion_fecha = tk.StringVar()

# Crear calendario
calendario = Calendar(root, locale="es")
calendario.config(background='black')
calendario.pack(pady=5, padx=5)

# Entry para colocar la fecha seleccionada
fecha_selector = tk.Entry(root, textvariable=seleccion_fecha)
fecha_selector.pack(pady=5)

# Establecer la fecha seleccionada en el entry
set_interval(establecer_fecha, 0.1)

# Crear botones para agregar, editar y borrar tareas
agregar_button = tk.Button(root, text="Agregar Tarea", command=agregar_tarea)
editar_button = tk.Button(root, text="Editar Tarea", command=editar_tarea)
borrar_button = tk.Button(root, text="Borrar Tarea", command=borrar_tarea)

agregar_button.config(pady=5, width=15)
editar_button.config(pady=5, width=15)
borrar_button.config(pady=5, width=15)

agregar_button.pack(pady=5)
editar_button.pack(pady=5)
borrar_button.pack(pady=5)

# Mostrar tareas
tarea_label = tk.Label(root, text="")
tarea_label.config(pady=10, bg='#333435', foreground='white')
tarea_label.pack()

actualizar_calendario()

root.mainloop()




