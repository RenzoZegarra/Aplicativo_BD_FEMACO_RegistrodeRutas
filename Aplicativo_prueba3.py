import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

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
# FUNCIONES DE CONSULTAS (12)
# --------------------------
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

# --------------------------
# FUNCIONES DE INSERCIÓN
# --------------------------
def insertar_conductor():
    try:
        nombre = entry_nombre_conductor.get()
        licencia = entry_licencia_conductor.get()
        telefono = entry_telefono_conductor.get()

        if not (nombre and licencia and telefono):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        sql = "INSERT INTO Conductor (nombre_conductor, licencia, telefono) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nombre, licencia, telefono))
        conexion.commit()
        messagebox.showinfo("Éxito", "Conductor agregado correctamente.")
        entry_nombre_conductor.delete(0, tk.END)
        entry_licencia_conductor.delete(0, tk.END)
        entry_telefono_conductor.delete(0, tk.END)
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

        if not (placa and marca and tonelaje and id_conductor and id_modelo):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        sql = "INSERT INTO Vehiculo (placa, marca, tonelaje, id_conductor, id_modelo, centro_costos) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (placa, marca, tonelaje, id_conductor, id_modelo, centro_costos))
        conexion.commit()
        messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")
        for e in [entry_placa, entry_marca, entry_tonelaje, entry_id_conductor, entry_id_modelo, entry_centro_costos]:
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

def insertar_ruta():
    try:
        descripcion = entry_descripcion_ruta.get()
        tipo = entry_tipo_ruta.get()
        kilometraje = entry_kilometraje.get()
        estado = entry_estado_ruta.get()

        if not (descripcion and tipo and kilometraje):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        sql = "INSERT INTO Ruta (descripcion, tipo_ruta, kilometraje, estado_ruta) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (descripcion, tipo, kilometraje, estado))
        conexion.commit()
        messagebox.showinfo("Éxito", "Ruta agregada correctamente.")
        for e in [entry_descripcion_ruta, entry_tipo_ruta, entry_kilometraje, entry_estado_ruta]:
            e.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")

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
tk.Label(frame_conductor, text="Licencia:", bg="#FFFBEA").pack()
entry_licencia_conductor = tk.Entry(frame_conductor)
entry_licencia_conductor.pack()
tk.Label(frame_conductor, text="Teléfono:", bg="#FFFBEA").pack()
entry_telefono_conductor = tk.Entry(frame_conductor)
entry_telefono_conductor.pack()
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

# Ejecutar ventana
ventana.mainloop()
