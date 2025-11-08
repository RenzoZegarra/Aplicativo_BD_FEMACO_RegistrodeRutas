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


# ----------------------
# Cabecera
# ----------------------
cabecera = tk.Label(
    ventana,
    text="FEMACO: Registro de Rutas",
    bg="green",        # mismo fondo que la ventana
    fg="white",        # color del texto
    font=("Arial", 30, "bold")  # fuente grande y negrita
)
cabecera.pack(fill="x", ipady=20)  # separa la cabecera del resto de elementos




# Botones
# Título 1: GESTIONAR BD
titulo = tk.Label(
    ventana,
    text="Gestionar Base de Datos",  
    fg="black",        # color del texto
    font=("Arial", 24, "bold")  
)
titulo.pack(pady=10)  # separa del resto de widgets

#BOTON DE CONEXION DE BD
btn_conectar = tk.Button(ventana, text="Conectar a BD", command=conectar_bd, bg="#4CAF50", fg="white")
btn_conectar.pack(pady=5)

# Título 2: MOSTRAR BD
titulo = tk.Label(
    ventana,
    text="Mostrar Base de Datos",  
    fg="black",        # color del texto
    font=("Arial", 24, "bold")  
)
titulo.pack(pady=10)  # separa del resto de widgets


# Título 3: GENERAR REPORTES
titulo = tk.Label(
    ventana,
    text="Generar Reportes de la BD",  
    fg="black",        # color del texto
    font=("Arial", 24, "bold")  
)
titulo.pack(pady=10)  # separa del resto de widgets

#BOTONES DE REPORTE/CONSULTA

#Consulta 1: Mostrar vehículos con conductor asignado
btn_consulta1 = tk.Button(ventana, text="Mostrar vehículos con conductor asignado", command=mostrar_Vehiculos_con_conductor, bg="#36f4ab", fg="white")
btn_consulta1.pack(pady=5)

#Consulta 2: Mostrar las rutas activas.
btn_consulta2 = tk.Button(ventana, text="Mostrar las rutas activas", command=mostrar_rutas_activas, bg="#e32813", fg="white")
btn_consulta2.pack(pady=5)

#Consulta 3: Mostrar detalles de las rutas.
btn_consulta3 = tk.Button(ventana, text="Mostrar detalles de las rutas", command=mostrar_detalles_rutas, bg="#e32813", fg="white")
btn_consulta3.pack(pady=5)

#Consulta 4: Mostrar las 3 rutas con el mejor rendimiento.
btn_consulta4 = tk.Button(ventana, text="Mostrar las 3 rutas con el mejor rendimiento", command=mostrar_rutas_con_mejor_rendimiento, bg="#e32813", fg="white")
btn_consulta4.pack(pady=5)

#Consulta 5: Mostrar los vehículos con su modelo y centro de costos.
btn_consulta5 = tk.Button(ventana, text="Mostrar los vehículos con su modelo y centro de costos.", command=mostrar_vehiculos_modelo, bg="#e32813", fg="white")
btn_consulta5.pack(pady=5)

#Consulta 6: Mostrar los modelos más usados por vehículos.
btn_consulta6 = tk.Button(ventana, text="Mostrar los modelos más usados por vehículos.", command=mostrar_modelos_mas_usados, bg="#e32813", fg="white")
btn_consulta6.pack(pady=5)

#Consulta 7: Mostrar el consumo promedio por modelo en todas las rutas.
btn_consulta7 = tk.Button(ventana, text="Mostrar el consumo promedio por modelo en todas las rutas", command=mostrar_consumo_promedio_modelos, bg="#e32813", fg="white")
btn_consulta7.pack(pady=5)

#Consulta 8: Mostrar los vehículos con tonelaje superior a 8 toneladas.
btn_consulta8 = tk.Button(ventana, text="Mostrar los vehículos con tonelaje superior a 8 toneladas", command=mostrar_vehiculos_pesados, bg="#e32813", fg="white")
btn_consulta8.pack(pady=5)

#Consulta 9: Mostrar las rutas por tipo (local o provincial) con cantidad total.
btn_consulta9 = tk.Button(ventana, text="Mostrar las rutas por tipo(local o provincial) con cantidad total", command=mostrar_rutas_por_tipo, bg="#e32813", fg="white")
btn_consulta9.pack(pady=5)

#Consulta 10: Mostrar las rutas inactivas.
btn_consulta10 = tk.Button(ventana, text="Mostrar las rutas inactivas", command=mostrar_rutas_inactivas, bg="#e32813", fg="white")
btn_consulta10.pack(pady=5)

#Consulta 11: Mostrar los vehículos agrupados por modelo.
btn_consulta11 = tk.Button(ventana, text="Mostrar los vehículos agrupados por modelo.", command=mostrar_vehiculos_por_modelo, bg="#e32813", fg="white")
btn_consulta11.pack(pady=5)

#Consulta 12: Buscar un modelo específico.
btn_consulta12 = tk.Button(ventana, text="Buscar un modelo específico.", command=buscar_modelo_especifico, bg="#e32813", fg="white")
btn_consulta12.pack(pady=5)

#BOTON DE CERRAR CONEXION CON LA BASE DE DATOS
btn_cerrar = tk.Button(ventana, text="Cerrar Conexión", command=cerrar_conexion, bg="#f44336", fg="white")
btn_cerrar.pack(pady=5)



# Cuadro de texto para mostrar resultados
texto = tk.Text(ventana, height=10, width=80)
texto.pack(pady=10)

# Ejecutar ventana
ventana.mainloop()
