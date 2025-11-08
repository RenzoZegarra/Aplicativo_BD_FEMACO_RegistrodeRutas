import tkinter as tk
from tkinter import messagebox
import mysql.connector

# --------------------------
# Función: Conectar a la base
# --------------------------
def conectar_bd():
    try:
        global conexion, cursor
        conexion = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='femaco_registro_de_rutas',
            port='3306'
        )
        if conexion.is_connected():
            messagebox.showinfo("Conexión", "Conectado correctamente a la base de datos")
            cursor = conexion.cursor()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar:\n{e}")

# --------------------------
# FUNCIONES DE CONSULTAS
# --------------------------

#Función consulta de mostrar conductores
def mostrar_conductores():
    try:
        cursor.execute("SELECT * FROM conductor")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)  # Limpia el texto anterior
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")

# --------------------------
# Función: Cerrar conexión
# --------------------------
def cerrar_conexion():
    try:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            messagebox.showinfo("Conexión", "Conexión cerrada correctamente")
    except:
        pass

# --------------------------
# Interfaz gráfica
# --------------------------
ventana = tk.Tk()
ventana.title("Registro de Conductores")
ventana.geometry("400x300")

# Botones
btn_conectar = tk.Button(ventana, text="Conectar a BD", command=conectar_bd, bg="#4CAF50", fg="white")
btn_conectar.pack(pady=5)

btn_mostrar = tk.Button(ventana, text="Mostrar Conductores", command=mostrar_conductores, bg="#2196F3", fg="white")
btn_mostrar.pack(pady=5)

btn_cerrar = tk.Button(ventana, text="Cerrar Conexión", command=cerrar_conexion, bg="#f44336", fg="white")
btn_cerrar.pack(pady=5)

# Cuadro de texto para mostrar resultados
texto = tk.Text(ventana, height=10, width=45)
texto.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()
