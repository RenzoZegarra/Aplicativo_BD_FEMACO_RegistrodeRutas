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


#Función Consulta 1: Vehículos que tienen conductor asignado.
def mostrar_Vehiculos_con_conductor():
    try:
        cursor.execute("SELECT v.placa, v.marca, v.tonelaje, c.nombre_conductor FROM Vehiculo v INNER JOIN Conductor c ON v.id_conductor = c.id_conductor")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")
        

#Función Consulta 2: Rutas que están activas actualmente.
def mostrar_rutas_activas():
    try:
        cursor.execute("SELECT id_ruta, descripcion, tipo_ruta, kilometraje FROM Ruta WHERE estado_ruta = 1")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)  # Limpia el texto anterior
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")

#Función Consulta 3: Descripción de las rutas y cuántos detalles tiene cada una.
def mostrar_detalles_rutas():
    try:
        cursor.execute("SELECT r.descripcion, COUNT(d.id_detalle) AS cantidad_detalles FROM Ruta r LEFT JOIN Detalle d ON r.id_ruta = d.id_ruta GROUP BY r.id_ruta, r.descripcion")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)  # Limpia el texto anterior
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")

#Función Consulta 4: Las 3 rutas con mejor rendimiento
def mostrar_rutas_con_mejor_rendimiento():
    try:
        cursor.execute("SELECT r.descripcion, r.kilometraje, ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio, ROUND(r.kilometraje / AVG(d.consumo_por_modelo), 2) AS rendimiento FROM Ruta r INNER JOIN Detalle d ON r.id_ruta = d.id_ruta GROUP BY r.id_ruta, r.descripcion, r.kilometraje ORDER BY rendimiento DESC LIMIT 3")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)  # Limpia el texto anterior
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")

#Función Consulta 5: 
def mostrar_vehiculos_modelo():
    try:
        cursor.execute("SELECT v.placa, v.marca, m.modelo_descripcion, v.centro_costos FROM Vehiculo v INNER JOIN Modelo m ON v.id_modelo = m.id_modelo;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 6
def mostrar_modelos_mas_usados():
    try:
        cursor.execute("SELECT m.modelo_descripcion, COUNT(v.placa) AS cantidad_vehiculos FROM Modelo m LEFT JOIN Vehiculo v ON m.id_modelo = v.id_modelo GROUP BY m.id_modelo, m.modelo_descripcion ORDER BY cantidad_vehiculos DESC;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 7
def mostrar_consumo_promedio_modelos():
    try:
        cursor.execute("SELECT m.modelo_descripcion, ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio FROM Modelo m INNER JOIN Detalle d ON m.id_modelo = d.id_modelo GROUP BY m.id_modelo, m.modelo_descripcion ORDER BY consumo_promedio ASC;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 8
def mostrar_vehiculos_pesados():
    try:
        cursor.execute("SELECT placa, marca, tonelaje, centro_costos FROM Vehiculo WHERE tonelaje > 8;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 9
def mostrar_rutas_por_tipo():
    try:
        cursor.execute("SELECT tipo_ruta, COUNT(*) AS cantidad_rutas FROM Ruta GROUP BY tipo_ruta;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 10
def mostrar_rutas_inactivas():
    try:
        cursor.execute("SELECT id_ruta, descripcion, tipo_ruta, kilometraje FROM Ruta WHERE estado_ruta = 0;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 11
def mostrar_vehiculos_por_modelo():
    try:
        cursor.execute("SELECT v.id_modelo, COUNT(*) AS cantidad FROM Vehiculo v GROUP BY v.id_modelo;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
        for fila in registros:
            texto.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")


#Función Consulta 12
def buscar_modelo_especifico():
    try:
        cursor.execute("SELECT * FROM Modelo WHERE id_modelo = 10;")
        registros = cursor.fetchall()
        texto.delete("1.0", tk.END)
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
ventana.state("zoomed")
ventana.config(bg="#E8CB79")

# --------------------------
# CONTENEDOR CON SCROLLBAR
# --------------------------
# Canvas que contendrá el frame desplazable
canvas = tk.Canvas(ventana, bg="#E8CB79", highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)

# Scrollbar vertical
scrollbar = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")

# Configurar el canvas para usar la scrollbar
canvas.configure(yscrollcommand=scrollbar.set)

# Frame dentro del canvas (donde pondremos los botones, labels, etc.)
frame_contenido = tk.Frame(canvas, bg="#E8CB79")
canvas.create_window((0, 0), window=frame_contenido, anchor="nw")

# Actualizar el área de scroll cuando cambia el tamaño
def actualizar_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame_contenido.bind("<Configure>", actualizar_scroll)

# Permitir scroll con la rueda del ratón
def scroll_con_rueda(event):
    canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

canvas.bind_all("<MouseWheel>", scroll_con_rueda)


# ----------------------
# Cabecera
# ----------------------
cabecera = tk.Label(
    frame_contenido,
    text="FEMACO: Registro de Rutas",
    bg="green",
    fg="white",
    font=("Arial", 30, "bold")
)
cabecera.pack(fill="x", ipady=20)

# ----------------------
# Botones y secciones
# ----------------------

# Título 1: GESTIONAR BD
titulo = tk.Label(
    frame_contenido,
    text="Gestionar Base de Datos",
    fg="black",
    font=("Arial", 24, "bold"),
    bg="#E8CB79"
)
titulo.pack(pady=10)

btn_conectar = tk.Button(frame_contenido, text="Conectar a BD", bg="#4CAF50", fg="white")
btn_conectar.pack(pady=5)

# Título 2: MOSTRAR BD
titulo = tk.Label(
    frame_contenido,
    text="Mostrar Base de Datos",
    fg="black",
    font=("Arial", 24, "bold"),
    bg="#E8CB79"
)
titulo.pack(pady=10)

# Título 3: GENERAR REPORTES
titulo = tk.Label(
    frame_contenido,
    text="Generar Reportes de la BD",
    fg="black",
    font=("Arial", 24, "bold"),
    bg="#E8CB79"
)
titulo.pack(pady=10)

# Ejemplo de botones de consulta
for i in range(1, 13):
    tk.Button(
        frame_contenido,
        text=f"Consulta {i}",
        bg="#e32813",
        fg="white"
    ).pack(pady=5)

# Botón de cerrar conexión
btn_cerrar = tk.Button(frame_contenido, text="Cerrar Conexión", bg="#f44336", fg="white")
btn_cerrar.pack(pady=10)

# Cuadro de texto para mostrar resultados
texto = tk.Text(frame_contenido, height=10, width=80)
texto.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()