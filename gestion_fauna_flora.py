import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Conexión a la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Conexion.2024.@",
    database="semana8"
)

cursor = db.cursor()

# Crear la ventana principal
root = tk.Tk()
root.title("Gestión de Fauna y Flora")

# Etiquetas y campos de entrada
labels = ["ID", "Nombre Científico", "Habitat", "Estado de Conservación", "Región Geográfica"]
entries = {}

for i, label in enumerate(labels):
    tk.Label(root, text=label).grid(row=i, column=0, padx=10, pady=5)
    entry = tk.Entry(root)
    entry.grid(row=i, column=1, padx=10, pady=5)
    entries[label] = entry

# Función para agregar objeto de fauna/flora
def agregar_objeto():
    valores = [entry.get() for entry in entries.values()]
    try:
        cursor.execute("INSERT INTO FaunaFlora (ID, NombreCientifico, Habitat, EstadoConservacion, RegionGeografica) VALUES (%s, %s, %s, %s, %s)", valores)
        db.commit()
        messagebox.showinfo("Éxito", "Objeto agregado exitosamente.")
        listar_objetos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error al agregar objeto: {err}")

# Función para listar objetos de fauna/flora
def listar_objetos():
    cursor.execute("SELECT * FROM FaunaFlora")
    registros = cursor.fetchall()
    lista.delete(0, tk.END)
    for registro in registros:
        lista.insert(tk.END, registro)

# Función para borrar objeto de fauna/flora
def borrar_objeto():
    seleccionado = lista.curselection()
    if seleccionado:
        valor = lista.get(seleccionado)
        cursor.execute("DELETE FROM FaunaFlora WHERE ID = %s", (valor[0],))
        db.commit()
        messagebox.showinfo("Éxito", "Objeto borrado exitosamente.")
        listar_objetos()

# Función para actualizar objeto de fauna/flora
def actualizar_objeto():
    seleccionado = lista.curselection()
    if seleccionado:
        valores = [entry.get() for entry in entries.values()]
        cursor.execute("""
            UPDATE FaunaFlora
            SET NombreCientifico = %s, Habitat = %s, EstadoConservacion = %s, RegionGeografica = %s
            WHERE ID = %s
        """, (valores[1], valores[2], valores[3], valores[4], valores[0]))
        db.commit()
        messagebox.showinfo("Éxito", "Objeto actualizado exitosamente.")
        listar_objetos()

# Botones para las operaciones CRUD
tk.Button(root, text="Agregar", command=agregar_objeto).grid(row=5, column=0, padx=10, pady=5)
tk.Button(root, text="Actualizar", command=actualizar_objeto).grid(row=5, column=1, padx=10, pady=5)
tk.Button(root, text="Borrar", command=borrar_objeto).grid(row=6, column=0, padx=10, pady=5)

# Lista para mostrar objetos de fauna/flora
lista = tk.Listbox(root, width=50)
lista.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

# Cargar la lista inicialmente
listar_objetos()

# Ejecutar la aplicación
root.mainloop()

# Cerrar la conexión a la base de datos al finalizar
cursor.close()
db.close()
