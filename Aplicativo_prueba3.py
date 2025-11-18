import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# --------------------------
# CONEXIÓN A LA BASE DE DATOS
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
            cursor = conexion.cursor()
            messagebox.showinfo("Conexión", "Conectado correctamente a la base de datos")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo conectar:\n{e}")

def cerrar_conexion():
    try:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            messagebox.showinfo("Conexión", "Conexión cerrada correctamente")
    except:
        pass

# --------------------------
# FUNCIÓN GENERAL PARA CONSULTAS
# --------------------------
def ejecutar_consulta(sql):
    try:
        cursor.execute(sql)
        registros = cursor.fetchall()
        texto_resultados.delete("1.0", tk.END)
        for fila in registros:
            texto_resultados.insert(tk.END, str(fila) + "\n")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo obtener datos:\n{e}")

# --------------------------
# CRUDS
# --------------------------
# CREATE: Inserciones
def insertar_conductor():
    try:
        nombre = entry_nombre_conductor.get()
        if not (nombre, ):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        sql = "INSERT INTO Conductor (nombre_conductor) VALUES (%s)"
        cursor.execute(sql, (nombre, ))
        conexion.commit()
        messagebox.showinfo("Éxito", "Conductor agregado correctamente.")
        entry_nombre_conductor.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")




def insertar_vehiculo():
    try:
        placa = entry_placa.get()
        marca = entry_marca.get()
        tonelaje = entry_tonelaje.get()
        id_conductor = entry_id_conductor.get()
        id_modelo = entry_id_modelo.get()
        centro_costos = entry_centro_costos.get()

        if not (placa and id_conductor and id_modelo and marca and tonelaje and centro_costos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        sql = "INSERT INTO Vehiculo (placa, id_conductor, id_modelo, marca, tonelaje, centro_costos) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, id_conductor, id_modelo, marca, tonelaje, centro_costos))
        conexion.commit()
        messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")
        for e in [entry_placa, entry_id_conductor, entry_id_modelo, entry_marca, entry_tonelaje, entry_centro_costos]:
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

def insertar_ruta():
    try:
        descripcion = entry_descripcion_ruta.get()
        tipo = entry_tipo_ruta.get()
        kilometraje = entry_kilometraje.get()
        estado = entry_estado_ruta.get()

        if not (kilometraje and tipo and descripcion and estado):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        sql = "INSERT INTO Ruta (kilometraje, tipo_ruta, descripcion, estado_ruta) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (kilometraje, tipo, descripcion, estado))
        conexion.commit()
        messagebox.showinfo("Éxito", "Ruta agregada correctamente.")
        for e in [entry_kilometraje, entry_tipo_ruta, entry_descripcion_ruta, entry_estado_ruta]:
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

def insertar_modelo():
    try:
        descripcion_modelo = entry_modelo_descripcion.get().strip()

        # Validación
        if not descripcion_modelo:
            messagebox.showwarning("Campos vacíos", "Ingrese una descripción válida.")
            return

        # Consulta SQL
        sql = "INSERT INTO Modelo (modelo_descripcion) VALUES (%s)"
        cursor.execute(sql, (descripcion_modelo,))
        conexion.commit()

        messagebox.showinfo("Éxito", "Modelo agregado correctamente.")
        entry_modelo_descripcion.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar el modelo:\n{e}")


def insertar_detalle():
    try:
        ruta = entry_id_ruta.get().strip()
        modelo = entry_id_modelo.get().strip()
        consumo = entry_consumo_por_modelo.get().strip()

        # Validaciones
        if not ruta or not modelo or not consumo:
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        if not ruta.isdigit() or not modelo.isdigit():
            messagebox.showwarning("Valor inválido", "ID Ruta y ID Modelo deben ser números enteros.")
            return

        # Validar decimal
        try:
            consumo_val = float(consumo)
        except ValueError:
            messagebox.showwarning("Valor inválido", "El consumo debe ser un número decimal válido.")
            return

        # Consulta SQL
        sql = """
            INSERT INTO Detalle (id_ruta, id_modelo, consumo_por_modelo)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql, (int(ruta), int(modelo), consumo_val))
        conexion.commit()

        messagebox.showinfo("Éxito", "Detalle agregado correctamente.")

        # Limpiar campos
        entry_id_ruta.delete(0, tk.END)
        entry_id_modelo.delete(0, tk.END)
        entry_consumo_por_modelo.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar el detalle:\n{e}")




#READ: Consultas

def consulta_vehiculos_con_conductor():
    ejecutar_consulta("SELECT v.placa, v.marca, v.tonelaje, c.nombre_conductor FROM Vehiculo v INNER JOIN Conductor c ON v.id_conductor = c.id_conductor;")

def consulta_rutas_activas():
    ejecutar_consulta("SELECT id_ruta, descripcion, tipo_ruta, kilometraje FROM Ruta WHERE estado_ruta = 1;")

def consulta_detalles_rutas():
    ejecutar_consulta("SELECT r.descripcion, COUNT(d.id_detalle) AS cantidad_detalles FROM Ruta r LEFT JOIN Detalle d ON r.id_ruta = d.id_ruta GROUP BY r.id_ruta, r.descripcion;")

def consulta_top_rendimiento():
    ejecutar_consulta("SELECT r.descripcion, r.kilometraje, ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio, ROUND(r.kilometraje / AVG(d.consumo_por_modelo), 2) AS rendimiento FROM Ruta r INNER JOIN Detalle d ON r.id_ruta = d.id_ruta GROUP BY r.id_ruta, r.descripcion, r.kilometraje ORDER BY rendimiento DESC LIMIT 3;")

def consulta_vehiculos_modelo():
    ejecutar_consulta("SELECT v.placa, v.marca, m.modelo_descripcion, v.centro_costos FROM Vehiculo v INNER JOIN Modelo m ON v.id_modelo = m.id_modelo;")

def consulta_modelos_usados():
    ejecutar_consulta("SELECT m.modelo_descripcion, COUNT(v.placa) AS cantidad_vehiculos FROM Modelo m LEFT JOIN Vehiculo v ON m.id_modelo = v.id_modelo GROUP BY m.id_modelo, m.modelo_descripcion ORDER BY cantidad_vehiculos DESC;")

def consulta_consumo_promedio():
    ejecutar_consulta("SELECT m.modelo_descripcion, ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio FROM Modelo m INNER JOIN Detalle d ON m.id_modelo = d.id_modelo GROUP BY m.id_modelo, m.modelo_descripcion ORDER BY consumo_promedio ASC;")

def consulta_vehiculos_pesados():
    ejecutar_consulta("SELECT placa, marca, tonelaje, centro_costos FROM Vehiculo WHERE tonelaje > 8;")

def consulta_rutas_tipo():
    ejecutar_consulta("SELECT tipo_ruta, COUNT(*) AS cantidad_rutas FROM Ruta GROUP BY tipo_ruta;")

def consulta_rutas_inactivas():
    ejecutar_consulta("SELECT id_ruta, descripcion, tipo_ruta, kilometraje FROM Ruta WHERE estado_ruta = 0;")

def consulta_vehiculos_por_modelo():
    ejecutar_consulta("SELECT v.id_modelo, COUNT(*) AS cantidad FROM Vehiculo v GROUP BY v.id_modelo;")

def consulta_modelo_especifico():
    ejecutar_consulta("SELECT * FROM Modelo WHERE id_modelo = 10;")

#Consultas de todas las tablas
def consulta_ruta():
    ejecutar_consulta("SELECT * FROM  ruta;")

def consulta_vehiculo():
    ejecutar_consulta("SELECT * FROM  vehiculo;")

def consulta_conductor():
    ejecutar_consulta("SELECT * FROM  conductor;")

def consulta_modelo():
    ejecutar_consulta("SELECT * FROM  modelo;")

def consulta_detalle():
    ejecutar_consulta("SELECT * FROM  detalle;")

#UPDATE
#Actualizar Conductor
def actualizar_conductor():
    conectar_bd()

    id_conductor = entry_id_conductor_act.get()
    nuevo_nombre = entry_nombre_conductor_act.get()

    try:
        sql = "UPDATE Conductor SET nombre_conductor=%s WHERE id_conductor=%s"
        cursor.execute(sql, (nuevo_nombre, id_conductor))
        conexion.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Conductor actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un conductor con ese ID")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Ruta
def actualizar_ruta():
    conectar_bd()

    id_ruta = entry_id_ruta_act.get()
    nuevo_km = entry_km_ruta_act.get()
    nuevo_tipo = entry_tipo_ruta_act.get()
    nueva_desc = entry_desc_ruta_act.get()
    nuevo_estado = entry_estado_ruta_act.get()

    try:
        sql = """UPDATE Ruta 
                 SET kilometraje=%s, tipo_ruta=%s, descripcion=%s, estado_ruta=%s
                 WHERE id_ruta=%s"""
        cursor.execute(sql, (nuevo_km, nuevo_tipo, nueva_desc, nuevo_estado, id_ruta))
        conexion.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Ruta actualizada correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe una ruta con ese ID")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")




#Actualizar Vehículo
def actualizar_vehiculo():
    conectar_bd()

    placa = entry_placa_act.get()
    marca = entry_marca_act.get()
    tonelaje = entry_tonelaje_act.get()
    id_conductor = entry_conductor_act.get()
    id_modelo = entry_modelo_act.get()
    centro_costos = entry_cc_act.get()

    try:
        sql = """UPDATE Vehiculo 
                 SET marca=%s, tonelaje=%s, id_conductor=%s, id_modelo=%s, centro_costos=%s
                 WHERE placa=%s"""
        cursor.execute(sql, (marca, tonelaje, id_conductor, id_modelo, centro_costos, placa))
        conexion.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Vehículo actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un vehículo con esa placa")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Modelo
def actualizar_modelo():
    conectar_bd()

    id_modelo = entry_id_modelo_act.get()
    nuevo_desc = entry_desc_modelo_act.get()

    try:
        sql = "UPDATE Modelo SET modelo_descripcion=%s WHERE id_modelo=%s"
        cursor.execute(sql, (nuevo_desc, id_modelo))
        conexion.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Modelo actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un modelo con ese ID")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Detalle
def actualizar_detalle():
    conectar_bd()

    id_detalle = entry_id_detalle_act.get()
    id_ruta = entry_id_ruta_det_act.get()
    id_modelo = entry_id_modelo_det_act.get()
    consumo = entry_consumo_det_act.get()

    try:
        sql = """UPDATE Detalle 
                 SET id_ruta=%s, id_modelo=%s, consumo_por_modelo=%s
                 WHERE id_detalle=%s"""
        cursor.execute(sql, (id_ruta, id_modelo, consumo, id_detalle))
        conexion.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Detalle actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un detalle con ese ID")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#DELETE: Borrados lógicos

#Eliminar Detalle
def eliminar_detalle():
    conectar_bd()
    id_detalle = entry_id_detalle_del.get()
    try:
        cursor.callproc("sp_eliminar_detalle", (id_detalle,))
        conexion.commit()
        messagebox.showinfo("Eliminar", "Detalle eliminado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")



#Eliminar Conductor
def eliminar_conductor():
    conectar_bd()
    id_conductor = entry_id_conductor_del.get()

    try:
        cursor.callproc("sp_eliminar_conductor", (id_conductor,))
        conexion.commit()
        messagebox.showinfo("Eliminar", "Conductor eliminado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


#Eliminar Modelo
def eliminar_modelo():
    conectar_bd()
    id_modelo = entry_id_modelo_del.get()
    try:
        cursor.callproc("sp_eliminar_modelo", (id_modelo,))
        conexion.commit()
        messagebox.showinfo("Eliminar", "Modelo eliminado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


#Eliminar Ruta
def eliminar_ruta():
    conectar_bd()
    id_ruta = entry_id_ruta_del.get()
    try:
        cursor.callproc("sp_eliminar_ruta", (id_ruta,))
        conexion.commit()
        messagebox.showinfo("Eliminar", "Ruta eliminada correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")


#Eliminar Vehículo
def eliminar_vehiculo():
    conectar_bd()
    placa = entry_placa_del.get()
    try:
        cursor.callproc("sp_eliminar_vehiculo", (placa,))
        conexion.commit()
        messagebox.showinfo("Eliminar", "Vehículo eliminado correctamente")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar:\n{e}")




# --------------------------
# INTERFAZ GRÁFICA
# --------------------------
ventana = tk.Tk()
ventana.title("FEMACO: Registro de Rutas")
ventana.state("zoomed")
ventana.config(bg="#E8CB79")

# Notebook (pestañas)
notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True, padx=10, pady=10)

# === Pestaña de Conexión ===
frame_conexion = tk.Frame(notebook, bg="#F7E7A8")
notebook.add(frame_conexion, text="Conexión")

tk.Label(frame_conexion, text="Gestión de Conexión", bg="#F7E7A8", font=("Arial", 20, "bold")).pack(pady=20)
tk.Button(frame_conexion, text="Conectar a BD", command=conectar_bd, bg="#4CAF50", fg="white", font=("Arial", 14)).pack(pady=10)
tk.Button(frame_conexion, text="Cerrar Conexión", command=cerrar_conexion, bg="#f44336", fg="white", font=("Arial", 14)).pack(pady=10)

# === Pestaña de Consultas ===
frame_consultas = tk.Frame(notebook, bg="#F7E7A8")
notebook.add(frame_consultas, text="Consultas")

frame_botones = tk.Frame(frame_consultas, bg="#F7E7A8")
frame_botones.pack(side="left", fill="y", padx=10, pady=10)

frame_texto = tk.Frame(frame_consultas)
frame_texto.pack(side="right", fill="both", expand=True, padx=10, pady=10)

scroll = tk.Scrollbar(frame_texto)
scroll.pack(side="right", fill="y")

texto_resultados = tk.Text(frame_texto, wrap="none", yscrollcommand=scroll.set, font=("Consolas", 12))
texto_resultados.pack(fill="both", expand=True)
scroll.config(command=texto_resultados.yview)

# Botones de consulta
consultas = [
    ("TODAS LAS RUTAS", consulta_ruta),
    ("TODOS LOS DETALLES", consulta_detalle),
    ("TODOS LOS MODELOS", consulta_modelo),
    ("TODOS LOS VEHICULOS", consulta_vehiculo),
    ("TODOS LOS CONDUCTORES", consulta_conductor), 
    ("Vehículos con conductor asignado", consulta_vehiculos_con_conductor),
    ("Rutas activas", consulta_rutas_activas),
    ("Detalles de rutas", consulta_detalles_rutas),
    ("Top 3 rutas con mejor rendimiento", consulta_top_rendimiento),
    ("Vehículos y su modelo", consulta_vehiculos_modelo),
    ("Modelos más usados", consulta_modelos_usados),
    ("Consumo promedio por modelo", consulta_consumo_promedio),
    ("Vehículos pesados", consulta_vehiculos_pesados),
    ("Rutas por tipo", consulta_rutas_tipo),
    ("Rutas inactivas", consulta_rutas_inactivas),
    ("Vehículos por modelo", consulta_vehiculos_por_modelo),
    ("Buscar modelo específico", consulta_modelo_especifico)
]

for texto, func in consultas:
    tk.Button(frame_botones, text=texto, command=func, bg="#1976D2", fg="white", width=35).pack(pady=2)

# === Pestaña de Inserción ===
frame_insertar = tk.Frame(notebook, bg="#F7E7A8")
notebook.add(frame_insertar, text="Insertar Datos")

# Subpestañas para insertar
tabs_insertar = ttk.Notebook(frame_insertar)
tabs_insertar.pack(fill="both", expand=True, padx=10, pady=10)

# --- Insertar Conductor ---
frame_conductor = tk.Frame(tabs_insertar, bg="#FFFBEA")
tabs_insertar.add(frame_conductor, text="Conductor")

tk.Label(frame_conductor, text="Agregar Conductor", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_conductor, text="Nombre:", bg="#FFFBEA").pack()
entry_nombre_conductor = tk.Entry(frame_conductor)
entry_nombre_conductor.pack()
tk.Button(frame_conductor, text="Guardar Conductor", bg="#4CAF50", fg="white", command=insertar_conductor).pack(pady=10)

# --- Insertar Vehículo ---
frame_vehiculo = tk.Frame(tabs_insertar, bg="#FFFBEA")
tabs_insertar.add(frame_vehiculo, text="Vehículo")

tk.Label(frame_vehiculo, text="Agregar Vehículo", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
campos_vehiculo = [("Placa:", 'placa'), ("Marca:", 'marca'), ("Tonelaje:", 'tonelaje'),
                   ("ID Conductor:", 'id_conductor'), ("ID Modelo:", 'id_modelo'), ("Centro Costos:", 'centro_costos')]
entries = {}
for texto, var in campos_vehiculo:
    tk.Label(frame_vehiculo, text=texto, bg="#FFFBEA").pack()
    entries[var] = tk.Entry(frame_vehiculo)
    entries[var].pack()

entry_placa = entries['placa']
entry_marca = entries['marca']
entry_tonelaje = entries['tonelaje']
entry_id_conductor = entries['id_conductor']
entry_id_modelo = entries['id_modelo']
entry_centro_costos = entries['centro_costos']

tk.Button(frame_vehiculo, text="Guardar Vehículo", bg="#4CAF50", fg="white", command=insertar_vehiculo).pack(pady=10)

# --- Insertar Ruta ---
frame_ruta = tk.Frame(tabs_insertar, bg="#FFFBEA")
tabs_insertar.add(frame_ruta, text="Ruta")

tk.Label(frame_ruta, text="Agregar Ruta", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_ruta, text="Descripción:", bg="#FFFBEA").pack()
entry_descripcion_ruta = tk.Entry(frame_ruta)
entry_descripcion_ruta.pack()
tk.Label(frame_ruta, text="Tipo de ruta:", bg="#FFFBEA").pack()
entry_tipo_ruta = tk.Entry(frame_ruta)
entry_tipo_ruta.pack()
tk.Label(frame_ruta, text="Kilometraje:", bg="#FFFBEA").pack()
entry_kilometraje = tk.Entry(frame_ruta)
entry_kilometraje.pack()
tk.Label(frame_ruta, text="Estado (1=Activo, 0=Inactivo):", bg="#FFFBEA").pack()
entry_estado_ruta = tk.Entry(frame_ruta)
entry_estado_ruta.pack()
tk.Button(frame_ruta, text="Guardar Ruta", bg="#4CAF50", fg="white", command=insertar_ruta).pack(pady=10)

#--- Insertar Modelo ---
frame_modelo = tk.Frame(tabs_insertar, bg="#FFFBEA")
tabs_insertar.add(frame_modelo, text="Modelo")

tk.Label(
    frame_modelo,
    text="Agregar Modelo",
    font=("Arial", 18, "bold"),
    bg="#FFFBEA"
).pack(pady=10)

tk.Label(
    frame_modelo,
    text="Descripción del Modelo:",
    bg="#FFFBEA"
).pack()

entry_modelo_descripcion = tk.Entry(frame_modelo)
entry_modelo_descripcion.pack()

tk.Button(
    frame_modelo,
    text="Guardar Modelo",
    bg="#4CAF50",
    fg="white",
    command=insertar_modelo
).pack(pady=10)

# --- Insertar Detalle ---
frame_detalle = tk.Frame(tabs_insertar, bg="#FFFBEA")
tabs_insertar.add(frame_detalle, text="Detalle")

tk.Label(
    frame_detalle,
    text="Agregar Detalle",
    font=("Arial", 18, "bold"),
    bg="#FFFBEA"
).pack(pady=10)

# ID Ruta
tk.Label(frame_detalle, text="ID Ruta:", bg="#FFFBEA").pack()
entry_id_ruta = tk.Entry(frame_detalle)
entry_id_ruta.pack()

# ID Modelo
tk.Label(frame_detalle, text="ID Modelo:", bg="#FFFBEA").pack()
entry_id_modelo = tk.Entry(frame_detalle)
entry_id_modelo.pack()

# Consumo por Modelo
tk.Label(frame_detalle, text="Consumo por Modelo:", bg="#FFFBEA").pack()
entry_consumo_por_modelo = tk.Entry(frame_detalle)
entry_consumo_por_modelo.pack()

# Botón Guardar
tk.Button(
    frame_detalle,
    text="Guardar Detalle",
    bg="#4CAF50",
    fg="white",
    command=insertar_detalle
).pack(pady=10)



# === Pestaña de Actualización ===
frame_actualizar = tk.Frame(notebook, bg="#F7E7A8")
notebook.add(frame_actualizar, text="Actualizar Datos")

tabs_actualizar = ttk.Notebook(frame_actualizar)
tabs_actualizar.pack(fill="both", expand=True, padx=10, pady=10)

# --- ACTUALIZAR CONDUCTOR ---
frame_act_conductor = tk.Frame(tabs_actualizar, bg="#FFFBEA")
tabs_actualizar.add(frame_act_conductor, text="Conductor")

tk.Label(frame_act_conductor, text="Actualizar Conductor", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_act_conductor, text="ID Conductor:", bg="#FFFBEA").pack()
entry_id_conductor_act = tk.Entry(frame_act_conductor)
entry_id_conductor_act.pack()
tk.Label(frame_act_conductor, text="Nuevo Nombre:", bg="#FFFBEA").pack()
entry_nombre_conductor_act = tk.Entry(frame_act_conductor)
entry_nombre_conductor_act.pack()
tk.Button(frame_act_conductor, text="Actualizar", bg="#0275D8", fg="white", command=actualizar_conductor).pack(pady=10)

# --- ACTUALIZAR MODELO ---
frame_act_modelo = tk.Frame(tabs_actualizar, bg="#FFFBEA")
tabs_actualizar.add(frame_act_modelo, text="Modelo")

tk.Label(frame_act_modelo, text="Actualizar Modelo", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_act_modelo, text="ID Modelo:", bg="#FFFBEA").pack()
entry_id_modelo_act = tk.Entry(frame_act_modelo)
entry_id_modelo_act.pack()
tk.Label(frame_act_modelo, text="Nueva Descripción:", bg="#FFFBEA").pack()
entry_desc_modelo_act = tk.Entry(frame_act_modelo)
entry_desc_modelo_act.pack()
tk.Button(frame_act_modelo, text="Actualizar", bg="#0275D8", fg="white", command=actualizar_modelo).pack(pady=10)

# --- ACTUALIZAR RUTA ---
frame_act_ruta = tk.Frame(tabs_actualizar, bg="#FFFBEA")
tabs_actualizar.add(frame_act_ruta, text="Ruta")

tk.Label(frame_act_ruta, text="Actualizar Ruta", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_act_ruta, text="ID Ruta:", bg="#FFFBEA").pack()
entry_id_ruta_act = tk.Entry(frame_act_ruta)
entry_id_ruta_act.pack()
tk.Label(frame_act_ruta, text="Kilometraje:", bg="#FFFBEA").pack()
entry_km_ruta_act = tk.Entry(frame_act_ruta)
entry_km_ruta_act.pack()
tk.Label(frame_act_ruta, text="Tipo de Ruta:", bg="#FFFBEA").pack()
entry_tipo_ruta_act = tk.Entry(frame_act_ruta)
entry_tipo_ruta_act.pack()
tk.Label(frame_act_ruta, text="Descripción:", bg="#FFFBEA").pack()
entry_desc_ruta_act = tk.Entry(frame_act_ruta)
entry_desc_ruta_act.pack()
tk.Label(frame_act_ruta, text="Estado (0/1):", bg="#FFFBEA").pack()
entry_estado_ruta_act = tk.Entry(frame_act_ruta)
entry_estado_ruta_act.pack()
tk.Button(frame_act_ruta, text="Actualizar", bg="#0275D8", fg="white", command=actualizar_ruta).pack(pady=10)

# --- ACTUALIZAR VEHICULO ---
frame_act_vehiculo = tk.Frame(tabs_actualizar, bg="#FFFBEA")
tabs_actualizar.add(frame_act_vehiculo, text="Vehículo")

tk.Label(frame_act_vehiculo, text="Actualizar Vehículo", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_act_vehiculo, text="Placa:", bg="#FFFBEA").pack()
entry_placa_act = tk.Entry(frame_act_vehiculo)
entry_placa_act.pack()
tk.Label(frame_act_vehiculo, text="Marca:", bg="#FFFBEA").pack()
entry_marca_act = tk.Entry(frame_act_vehiculo)
entry_marca_act.pack()
tk.Label(frame_act_vehiculo, text="Tonelaje:", bg="#FFFBEA").pack()
entry_tonelaje_act = tk.Entry(frame_act_vehiculo)
entry_tonelaje_act.pack()
tk.Label(frame_act_vehiculo, text="ID Conductor:", bg="#FFFBEA").pack()
entry_conductor_act = tk.Entry(frame_act_vehiculo)
entry_conductor_act.pack()
tk.Label(frame_act_vehiculo, text="ID Modelo:", bg="#FFFBEA").pack()
entry_modelo_act = tk.Entry(frame_act_vehiculo)
entry_modelo_act.pack()
tk.Label(frame_act_vehiculo, text="Centro de Costos:", bg="#FFFBEA").pack()
entry_cc_act = tk.Entry(frame_act_vehiculo)
entry_cc_act.pack()
tk.Button(frame_act_vehiculo, text="Actualizar", bg="#0275D8", fg="white", command=actualizar_vehiculo).pack(pady=10)

# --- ACTUALIZAR DETALLE ---
frame_act_detalle = tk.Frame(tabs_actualizar, bg="#FFFBEA")
tabs_actualizar.add(frame_act_detalle, text="Detalle")

tk.Label(frame_act_detalle, text="Actualizar Detalle", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_act_detalle, text="ID Detalle:", bg="#FFFBEA").pack()
entry_id_detalle_act = tk.Entry(frame_act_detalle)
entry_id_detalle_act.pack()
tk.Label(frame_act_detalle, text="ID Ruta:", bg="#FFFBEA").pack()
entry_id_ruta_det_act = tk.Entry(frame_act_detalle)
entry_id_ruta_det_act.pack()
tk.Label(frame_act_detalle, text="ID Modelo:", bg="#FFFBEA").pack()
entry_id_modelo_det_act = tk.Entry(frame_act_detalle)
entry_id_modelo_det_act.pack()
tk.Label(frame_act_detalle, text="Consumo por modelo:", bg="#FFFBEA").pack()
entry_consumo_det_act = tk.Entry(frame_act_detalle)
entry_consumo_det_act.pack()
tk.Button(frame_act_detalle, text="Actualizar", bg="#0275D8", fg="white", command=actualizar_detalle).pack(pady=10)


# === Pestaña de Eliminación ===
frame_eliminar = tk.Frame(notebook, bg="#F7E7A8")
notebook.add(frame_eliminar, text="Eliminar Datos")

tabs_eliminar = ttk.Notebook(frame_eliminar)
tabs_eliminar.pack(fill="both", expand=True, padx=10, pady=10)

# --- ELIMINAR CONDUCTOR ---
frame_del_conductor = tk.Frame(tabs_eliminar, bg="#FFFBEA")
tabs_eliminar.add(frame_del_conductor, text="Conductor")

tk.Label(frame_del_conductor, text="Eliminar Conductor", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_del_conductor, text="ID Conductor:", bg="#FFFBEA").pack()
entry_id_conductor_del = tk.Entry(frame_del_conductor)
entry_id_conductor_del.pack()
tk.Button(frame_del_conductor, text="Eliminar", bg="#D9534F", fg="white", command=eliminar_conductor).pack(pady=10)


# --- ELIMINAR MODELO ---
frame_del_modelo = tk.Frame(tabs_eliminar, bg="#FFFBEA")
tabs_eliminar.add(frame_del_modelo, text="Modelo")

tk.Label(frame_del_modelo, text="Eliminar Modelo", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_del_modelo, text="ID Modelo:", bg="#FFFBEA").pack()
entry_id_modelo_del = tk.Entry(frame_del_modelo)
entry_id_modelo_del.pack()
tk.Button(frame_del_modelo, text="Eliminar", bg="#D9534F", fg="white", command=eliminar_modelo).pack(pady=10)

# --- ELIMINAR RUTA ---
frame_del_ruta = tk.Frame(tabs_eliminar, bg="#FFFBEA")
tabs_eliminar.add(frame_del_ruta, text="Ruta")

tk.Label(frame_del_ruta, text="Eliminar Ruta", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_del_ruta, text="ID Ruta:", bg="#FFFBEA").pack()
entry_id_ruta_del = tk.Entry(frame_del_ruta)
entry_id_ruta_del.pack()
tk.Button(frame_del_ruta, text="Eliminar", bg="#D9534F", fg="white", command=eliminar_ruta).pack(pady=10)

# --- ELIMINAR VEHICULO ---
frame_del_vehiculo = tk.Frame(tabs_eliminar, bg="#FFFBEA")
tabs_eliminar.add(frame_del_vehiculo, text="Vehículo")

tk.Label(frame_del_vehiculo, text="Eliminar Vehículo", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_del_vehiculo, text="Placa:", bg="#FFFBEA").pack()
entry_placa_del = tk.Entry(frame_del_vehiculo)
entry_placa_del.pack()
tk.Button(frame_del_vehiculo, text="Eliminar", bg="#D9534F", fg="white", command=eliminar_vehiculo).pack(pady=10)

# --- ELIMINAR DETALLE ---
frame_del_detalle = tk.Frame(tabs_eliminar, bg="#FFFBEA")
tabs_eliminar.add(frame_del_detalle, text="Detalle")

tk.Label(frame_del_detalle, text="Eliminar Detalle", font=("Arial", 18, "bold"), bg="#FFFBEA").pack(pady=10)
tk.Label(frame_del_detalle, text="ID Detalle:", bg="#FFFBEA").pack()
entry_id_detalle_del = tk.Entry(frame_del_detalle)
entry_id_detalle_del.pack()
tk.Button(frame_del_detalle, text="Eliminar", bg="#D9534F", fg="white", command=eliminar_detalle).pack(pady=10)



# Ejecutar ventana
ventana.mainloop()
