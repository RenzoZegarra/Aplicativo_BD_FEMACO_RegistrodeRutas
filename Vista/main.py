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
def ejecutar_procedimiento(proc_nombre):
    """
    Ejecuta un procedimiento almacenado sin parámetros
    y muestra los resultados en texto_resultados.
    """
    try:
        texto_resultados.delete("1.0", tk.END)

        # Ejecutar procedimiento
        cursor.callproc(proc_nombre)

        # Iterar todos los resultados del procedimiento
        for result in cursor.stored_results():
            registros = result.fetchall()
            for fila in registros:
                texto_resultados.insert(tk.END, str(fila) + "\n")

        # Limpiar resultados pendientes
        while cursor.nextset():
            pass

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo ejecutar el procedimiento:\n{e}")

# --------------------------
# CRUDS
# --------------------------
# CREATE: Inserciones
def insertar_conductor():
    try:
        nombre = entry_nombre_conductor.get()
        if not nombre.strip():  # Validación más robusta
            messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
            return

        # Llamar al procedimiento almacenado
        cursor.callproc('insertar_conductor', (nombre,))
        conexion.commit()

        messagebox.showinfo("Éxito", "Conductor agregado correctamente.")
        entry_nombre_conductor.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")




def insertar_vehiculo():
    try:
        placa = entry_placa.get().strip()
        marca = entry_marca.get().strip()
        tonelaje = entry_tonelaje.get().strip()
        id_conductor = entry_id_conductor.get().strip()
        id_modelo = entry_id_modelo_vehiculo.get().strip()
        centro_costos = entry_centro_costos.get().strip()

        # DEBUG
        print("===== DEBUG CAMPOS =====")
        print("placa:", repr(placa))
        print("marca:", repr(marca))
        print("tonelaje:", repr(tonelaje))
        print("id_conductor:", repr(id_conductor))
        print("id_modelo:", repr(id_modelo))
        print("centro_costos:", repr(centro_costos))
        print("========================")


        # Validación correcta
        campos = [placa, marca, tonelaje, id_conductor, id_modelo, centro_costos]
        if any(c == "" for c in campos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        # Convertir a números
        id_conductor = int(id_conductor)
        id_modelo = int(id_modelo)
        tonelaje = int(tonelaje)

        # Llamar al procedimiento
        cursor.callproc("insertar_vehiculo", (placa, id_conductor, id_modelo, marca, tonelaje, centro_costos))
        conexion.commit()

        messagebox.showinfo("Éxito", "Vehículo agregado correctamente.")

        for e in [entry_placa, entry_marca, entry_tonelaje, entry_id_conductor, entry_id_modelo_vehiculo, entry_centro_costos]:
            e.delete(0, tk.END)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo insertar:\n{e}")


def insertar_ruta():
    try:
        descripcion = entry_descripcion_ruta.get().strip()
        tipo = entry_tipo_ruta.get().strip()
        kilometraje = entry_kilometraje.get().strip()
        estado = entry_estado_ruta.get().strip()

        # Validación correcta
        campos = [descripcion, tipo, kilometraje, estado]
        if any(c == "" for c in campos):
            messagebox.showwarning("Campos vacíos", "Complete todos los campos obligatorios.")
            return

        # Validación de números
        try:
            kilometraje = int(kilometraje)
            estado = int(estado)
        except ValueError:
            messagebox.showerror("Error", "Kilometraje y Estado deben ser números enteros.")
            return

        # Llamada al procedimiento almacenado
        cursor.callproc(
            'insertar_ruta',
            (kilometraje, tipo, descripcion, estado)
        )
        conexion.commit()

        messagebox.showinfo("Éxito", "Ruta agregada correctamente.")

        # Limpiar campos
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

        # Llamar al procedimiento almacenado
        cursor.callproc("insertar_modelo", (descripcion_modelo,))
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

        # Validación del consumo (decimal)
        try:
            consumo_val = float(consumo)
        except ValueError:
            messagebox.showwarning("Valor inválido", "El consumo debe ser un número decimal válido.")
            return

        # Llamar al procedimiento almacenado
        cursor.callproc(
            "insertar_detalle",
            (int(ruta), int(modelo), float(consumo_val))
        )
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
    ejecutar_procedimiento("consulta1_vehiculos_con_conductor")

def consulta_rutas_activas():
    ejecutar_procedimiento("consulta2_rutas_activas")

def consulta_detalles_rutas():
    ejecutar_procedimiento("consulta3_rutas_detalles")

def consulta_top_rendimiento():
    ejecutar_procedimiento("consulta4_top_rendimiento")

def consulta_vehiculos_modelo():
    ejecutar_procedimiento("consulta5_vehiculos_modelo")

def consulta_modelos_usados():
    ejecutar_procedimiento("consulta6_modelos_usados")

def consulta_consumo_promedio():
    ejecutar_procedimiento("consulta7_consumo_promedio_modelo")

def consulta_vehiculos_pesados():
    ejecutar_procedimiento("consulta8_vehiculos_tonelaje")

def consulta_rutas_tipo():
    ejecutar_procedimiento("consulta9_rutas_tipo")

def consulta_rutas_inactivas():
    ejecutar_procedimiento("consulta10_rutas_inactivas")

# Consultas de todas las tablas
def consulta_ruta():
    ejecutar_procedimiento("mostrar_todas_rutas")

def consulta_vehiculo():
    ejecutar_procedimiento("mostrar_todos_vehiculos")

def consulta_conductor():
    ejecutar_procedimiento("mostrar_todos_conductores")

def consulta_modelo():
    ejecutar_procedimiento("mostrar_todos_modelos")

def consulta_detalle():
    ejecutar_procedimiento("mostrar_todos_detalles")


#UPDATE
#Actualizar Conductor
def actualizar_conductor():
    conectar_bd()  

    id_conductor = entry_id_conductor_act.get().strip()
    nuevo_nombre = entry_nombre_conductor_act.get().strip()

    if not id_conductor or not nuevo_nombre:
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not id_conductor.isdigit():
        messagebox.showwarning("Valor inválido", "El ID del conductor debe ser un número entero.")
        return

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc("actualizar_conductor", (int(id_conductor), nuevo_nombre))
        conexion.commit()

        # Verificar si se actualizó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Conductor actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un conductor con ese ID")

        # Limpiar campos
        entry_id_conductor_act.delete(0, tk.END)
        entry_nombre_conductor_act.delete(0, tk.END)

        # Limpiar resultados pendientes (muy importante)
        while cursor.nextset():
            pass

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Ruta
def actualizar_ruta():
    conectar_bd()  

    id_ruta = entry_id_ruta_act.get().strip()
    nuevo_km = entry_km_ruta_act.get().strip()
    nuevo_tipo = entry_tipo_ruta_act.get().strip()
    nueva_desc = entry_desc_ruta_act.get().strip()
    nuevo_estado = entry_estado_ruta_act.get().strip()

    # Validaciones básicas
    if not (id_ruta and nuevo_km and nuevo_tipo and nueva_desc and nuevo_estado):
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not id_ruta.isdigit() or not nuevo_km.isdigit() or not nuevo_estado.isdigit():
        messagebox.showwarning("Valor inválido", "ID, kilometraje y estado deben ser números enteros.")
        return

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc(
            "actualizar_ruta",
            (int(id_ruta), int(nuevo_km), nuevo_tipo, nueva_desc, int(nuevo_estado))
        )
        conexion.commit()

        # Verificar si se actualizó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Ruta actualizada correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe una ruta con ese ID")

        # Limpiar campos
        entry_id_ruta_act.delete(0, tk.END)
        entry_km_ruta_act.delete(0, tk.END)
        entry_tipo_ruta_act.delete(0, tk.END)
        entry_desc_ruta_act.delete(0, tk.END)
        entry_estado_ruta_act.delete(0, tk.END)

        # Limpiar resultados pendientes
        while cursor.nextset():
            pass

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")




#Actualizar Vehículo
def actualizar_vehiculo():
    conectar_bd()  

    placa = entry_placa_act.get().strip()
    marca = entry_marca_act.get().strip()
    tonelaje = entry_tonelaje_act.get().strip()
    id_conductor = entry_conductor_act.get().strip()
    id_modelo = entry_modelo_act.get().strip()
    centro_costos = entry_cc_act.get().strip()

    # Validaciones básicas
    if not (placa and marca and tonelaje and id_conductor and id_modelo and centro_costos):
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not id_conductor.isdigit() or not id_modelo.isdigit() or not tonelaje.isdigit():
        messagebox.showwarning("Valor inválido", "Conductor, modelo y tonelaje deben ser números enteros.")
        return

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc(
            "actualizar_vehiculo",
            (placa, int(id_conductor), int(id_modelo), marca, int(tonelaje), centro_costos)
        )
        conexion.commit()

        # Verificar si se actualizó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Vehículo actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un vehículo con esa placa")

        # Limpiar campos
        entry_placa_act.delete(0, tk.END)
        entry_marca_act.delete(0, tk.END)
        entry_tonelaje_act.delete(0, tk.END)
        entry_conductor_act.delete(0, tk.END)
        entry_modelo_act.delete(0, tk.END)
        entry_cc_act.delete(0, tk.END)

        # Limpiar resultados pendientes
        while cursor.nextset():
            pass

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Modelo
def actualizar_modelo():
    conectar_bd()  

    id_modelo = entry_id_modelo_act.get().strip()
    nuevo_desc = entry_desc_modelo_act.get().strip()

    # Validaciones básicas
    if not id_modelo or not nuevo_desc:
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not id_modelo.isdigit():
        messagebox.showwarning("Valor inválido", "El ID del modelo debe ser un número entero.")
        return

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc("actualizar_modelo", (int(id_modelo), nuevo_desc))
        conexion.commit()

        # Verificar si se actualizó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Modelo actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un modelo con ese ID")

        # Limpiar campos
        entry_id_modelo_act.delete(0, tk.END)
        entry_desc_modelo_act.delete(0, tk.END)

        # Limpiar resultados pendientes
        while cursor.nextset():
            pass

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")



#Actualizar Detalle
def actualizar_detalle():
    conectar_bd()  

    id_detalle = entry_id_detalle_act.get().strip()
    id_ruta = entry_id_ruta_det_act.get().strip()
    id_modelo = entry_id_modelo_det_act.get().strip()
    consumo = entry_consumo_det_act.get().strip()

    # Validaciones básicas
    if not (id_detalle and id_ruta and id_modelo and consumo):
        messagebox.showwarning("Campos vacíos", "Complete todos los campos.")
        return

    if not (id_detalle.isdigit() and id_ruta.isdigit() and id_modelo.isdigit()):
        messagebox.showwarning("Valor inválido", "IDs de detalle, ruta y modelo deben ser números enteros.")
        return

    # Validar que consumo sea un número decimal
    try:
        consumo_val = float(consumo)
    except ValueError:
        messagebox.showwarning("Valor inválido", "El consumo debe ser un número decimal válido.")
        return

    try:
        # Llamar al procedimiento almacenado
        cursor.callproc("actualizar_detalle", (int(id_detalle), int(id_ruta), int(id_modelo), consumo_val))
        conexion.commit()

        # Verificar si se actualizó algún registro
        if cursor.rowcount > 0:
            messagebox.showinfo("Actualizar", "Detalle actualizado correctamente")
        else:
            messagebox.showwarning("Actualizar", "No existe un detalle con ese ID")

        # Limpiar campos
        entry_id_detalle_act.delete(0, tk.END)
        entry_id_ruta_det_act.delete(0, tk.END)
        entry_id_modelo_det_act.delete(0, tk.END)
        entry_consumo_det_act.delete(0, tk.END)

        # Limpiar resultados pendientes
        while cursor.nextset():
            pass

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




# ============================
#     INTERFAZ GRÁFICA
# ============================
ventana = tk.Tk()
ventana.title("FEMACO • Administrador de Base de Datos")
ventana.state("zoomed")
ventana.config(bg="#f5f3ed")  # Fondo suave y limpio

# --------------------------
#     ESTILOS MODERNOS
# --------------------------
style = ttk.Style()
style.theme_use("clam")

# Estilo para las pestañas
style.configure("TNotebook", background="#f5f3ed", borderwidth=0)
style.configure("TNotebook.Tab",
                font=("Segoe UI", 12, "bold"),
                padding=[15, 8],
                background="#d9d4c7")
style.map("TNotebook.Tab",
          background=[("selected", "#b89c5d")],
          foreground=[("selected", "white")])

# Estilo de botones
boton_estilo = {
    "font": ("Segoe UI", 12, "bold"),
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2",
    "fg": "white",
    "width": 18,
    "height": 2
}

# Notebook
notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True, padx=15, pady=15)

# =======================================
#          PESTAÑA 1: CONEXIÓN
# =======================================
frame_conexion = tk.Frame(notebook, bg="#faf7ef")
notebook.add(frame_conexion, text="🔌 Conexión")

tk.Label(
    frame_conexion,
    text="Panel de Gestión de Conexión",
    bg="#faf7ef",
    fg="#6c4f2d",
    font=("Segoe UI", 24, "bold")
).pack(pady=40)

tk.Button(
    frame_conexion,
    text="Conectar Base de Datos",
    command=conectar_bd,
    bg="#4b8f2f",
    **boton_estilo
).pack(pady=20)

tk.Button(
    frame_conexion,
    text="Cerrar Conexión",
    command=cerrar_conexion,
    bg="#c0392b",
    **boton_estilo
).pack(pady=20)

# =======================================
# PIE DE PÁGINA CORPORATIVO
# =======================================
footer = tk.Label(
    ventana,
    text="FEMACO © 2025  •  Sistema de Gestión de Rutas y Bases de Datos",
    bg="#f5f3ed",
    fg="#000000",
    font=("Segoe UI", 8)
)
footer.pack(side="bottom", pady=1)


# =======================================
#          PESTAÑA DE CONSULTAS
# =======================================

frame_consultas = tk.Frame(notebook, bg="#f0ebe1")
notebook.add(frame_consultas, text="📊 Consultar Datos")

# ==== Panel Izquierdo (Menú de Consultas) ====
menu_consultas = tk.Frame(frame_consultas, bg="#d6c7a1", width=280)
menu_consultas.pack(side="left", fill="y")
menu_consultas.pack_propagate(False)

tk.Label(
    menu_consultas,
    text="Consultas Disponibles",
    bg="#d6c7a1",
    fg="#3d2f1c",
    font=("Segoe UI", 16, "bold")
).pack(pady=20)

# ==== Estilo para los botones del menú ====
estilo_menu = {
    "font": ("Segoe UI", 11, "bold"),
    "bg": "#8e793e",
    "fg": "white",
    "activebackground": "#b89c5d",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "cursor": "hand2",
    "anchor": "w",
    "padx": 15,
    "width": 30
}

consultas = [
    ("📌 Todas las rutas", consulta_ruta),
    ("📌 Todos los detalles", consulta_detalle),
    ("📌 Todos los modelos", consulta_modelo),
    ("📌 Todos los vehículos", consulta_vehiculo),
    ("📌 Todos los conductores", consulta_conductor),
    ("🚗 Vehículos con conductor asignado", consulta_vehiculos_con_conductor),
    ("🛣️ Rutas activas", consulta_rutas_activas),
    ("📋 Detalles de rutas", consulta_detalles_rutas),
    ("🏆 Top 3 rutas por rendimiento", consulta_top_rendimiento),
    ("🚘 Vehículos y su modelo", consulta_vehiculos_modelo),
    ("🔥 Modelos más usados", consulta_modelos_usados),
    ("⛽ Consumo promedio por modelo", consulta_consumo_promedio),
    ("🚛 Vehículos pesados", consulta_vehiculos_pesados),
    ("🗂️ Rutas por tipo", consulta_rutas_tipo),
    ("⛔ Rutas inactivas", consulta_rutas_inactivas)
]

for texto, func in consultas:
    tk.Button(menu_consultas, text=texto, command=func, **estilo_menu).pack(pady=3)

# ===== Línea decorativa debajo del menú =====
tk.Frame(menu_consultas, bg="#b09b6d", height=2).pack(fill="x", padx=10, pady=15)



# =========================================================
#              Panel derecho – Área de resultados
# =========================================================

contenedor_resultados = tk.Frame(frame_consultas, bg="#f0ebe1")
contenedor_resultados.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Título dinámico
titulo_resultados = tk.Label(
    contenedor_resultados,
    text="Resultados de la consulta",
    bg="#f0ebe1",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold"),
    anchor="w"
)
titulo_resultados.pack(fill="x", pady=10)

# Marco con borde elegante
marco_texto = tk.Frame(contenedor_resultados, bg="#fff", bd=2, relief="groove")
marco_texto.pack(fill="both", expand=True)

scroll = tk.Scrollbar(marco_texto)
scroll.pack(side="right", fill="y")

texto_resultados = tk.Text(
    marco_texto,
    wrap="none",
    yscrollcommand=scroll.set,
    font=("Consolas", 12),
    bg="#fafafa",
    fg="#333"
)
texto_resultados.pack(fill="both", expand=True)
scroll.config(command=texto_resultados.yview)

# =======================================
#          PESTAÑA DE INSERCIÓN
# =======================================

frame_insertar = tk.Frame(notebook, bg="#f0ebe1")
notebook.add(frame_insertar, text="📝 Insertar Datos")

# Subpestañas (Notebook interno)
tabs_insertar = ttk.Notebook(frame_insertar)
tabs_insertar.pack(fill="both", expand=True, padx=15, pady=15)

# ---------------------------------------
#  ESTILO GENERAL PARA FORMULARIOS
# ---------------------------------------

form_style_label = {
    "bg": "#faf7ef",
    "fg": "#4a3b22",
    "font": ("Segoe UI", 11, "bold"),
    "anchor": "w"
}

form_style_entry = {
    "font": ("Segoe UI", 11),
    "bd": 1
}

button_style = {
    "font": ("Segoe UI", 12, "bold"),
    "bg": "#4b8f2f",
    "fg": "white",
    "activebackground": "#60a542",
    "relief": "flat",
    "cursor": "hand2",
    "width": 20,
    "height": 2
}


# ===================================================
#               --- INSERTAR CONDUCTOR ---
# ===================================================

frame_conductor = tk.Frame(tabs_insertar, bg="#faf7ef")
tabs_insertar.add(frame_conductor, text="👤 Conductor")

tk.Label(
    frame_conductor,
    text="Registro de Conductor",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form_conductor = tk.Frame(frame_conductor, bg="#faf7ef")
form_conductor.pack(pady=10)

tk.Label(form_conductor, text="Nombre del Conductor:", **form_style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_nombre_conductor = tk.Entry(form_conductor, **form_style_entry)
entry_nombre_conductor.grid(row=0, column=1, pady=5, padx=10)

tk.Button(
    frame_conductor,
    text="Guardar Conductor",
    command=insertar_conductor,
    **button_style
).pack(pady=15)


# ===================================================
#               --- INSERTAR VEHÍCULO ---
# ===================================================

frame_vehiculo = tk.Frame(tabs_insertar, bg="#faf7ef")
tabs_insertar.add(frame_vehiculo, text="🚗 Vehículo")

tk.Label(
    frame_vehiculo,
    text="Registro de Vehículo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form_vehiculo = tk.Frame(frame_vehiculo, bg="#faf7ef")
form_vehiculo.pack(pady=10)

campos_vehiculo = [
    ("Placa:", "placa"),
    ("Marca:", "marca"),
    ("Tonelaje:", "tonelaje"),
    ("ID Conductor:", "id_conductor"),
    ("ID Modelo:", "id_modelo"),
    ("Centro Costos:", "centro_costos")
]

entries = {}

for i, (label, var) in enumerate(campos_vehiculo):
    tk.Label(form_vehiculo, text=label, **form_style_label).grid(row=i, column=0, pady=5, sticky="w")
    entries[var] = tk.Entry(form_vehiculo, **form_style_entry)
    entries[var].grid(row=i, column=1, pady=5, padx=10)

entry_placa = entries["placa"]
entry_marca = entries["marca"]
entry_tonelaje = entries["tonelaje"]
entry_id_conductor = entries["id_conductor"]
entry_id_modelo_vehiculo = entries["id_modelo"]
entry_centro_costos = entries["centro_costos"]

tk.Button(
    frame_vehiculo,
    text="Guardar Vehículo",
    command=insertar_vehiculo,
    **button_style
).pack(pady=15)


# ===================================================
#                  --- INSERTAR RUTA ---
# ===================================================

frame_ruta = tk.Frame(tabs_insertar, bg="#faf7ef")
tabs_insertar.add(frame_ruta, text="🛣️ Ruta")

tk.Label(
    frame_ruta,
    text="Registro de Ruta",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form_ruta = tk.Frame(frame_ruta, bg="#faf7ef")
form_ruta.pack(pady=10)

tk.Label(form_ruta, text="Descripción:", **form_style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_descripcion_ruta = tk.Entry(form_ruta, **form_style_entry)
entry_descripcion_ruta.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form_ruta, text="Tipo de Ruta:", **form_style_label).grid(row=1, column=0, pady=5, sticky="w")
entry_tipo_ruta = tk.Entry(form_ruta, **form_style_entry)
entry_tipo_ruta.grid(row=1, column=1, pady=5, padx=10)

tk.Label(form_ruta, text="Kilometraje:", **form_style_label).grid(row=2, column=0, pady=5, sticky="w")
entry_kilometraje = tk.Entry(form_ruta, **form_style_entry)
entry_kilometraje.grid(row=2, column=1, pady=5, padx=10)

tk.Label(form_ruta, text="Estado (1=Activo, 0=Inactivo):", **form_style_label).grid(row=3, column=0, pady=5, sticky="w")
entry_estado_ruta = tk.Entry(form_ruta, **form_style_entry)
entry_estado_ruta.grid(row=3, column=1, pady=5, padx=10)

tk.Button(
    frame_ruta,
    text="Guardar Ruta",
    command=insertar_ruta,
    **button_style
).pack(pady=15)


# ===================================================
#                --- INSERTAR MODELO ---
# ===================================================

frame_modelo = tk.Frame(tabs_insertar, bg="#faf7ef")
tabs_insertar.add(frame_modelo, text="📦 Modelo")

tk.Label(
    frame_modelo,
    text="Registro de Modelo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form_modelo = tk.Frame(frame_modelo, bg="#faf7ef")
form_modelo.pack(pady=10)

tk.Label(form_modelo, text="Descripción del Modelo:", **form_style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_modelo_descripcion = tk.Entry(form_modelo, **form_style_entry)
entry_modelo_descripcion.grid(row=0, column=1, pady=5, padx=10)

tk.Button(
    frame_modelo,
    text="Guardar Modelo",
    command=insertar_modelo,
    **button_style
).pack(pady=15)


# ===================================================
#                --- INSERTAR DETALLE ---
# ===================================================

frame_detalle = tk.Frame(tabs_insertar, bg="#faf7ef")
tabs_insertar.add(frame_detalle, text="📑 Detalle")

tk.Label(
    frame_detalle,
    text="Registro de Detalle",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form_detalle = tk.Frame(frame_detalle, bg="#faf7ef")
form_detalle.pack(pady=10)

tk.Label(form_detalle, text="ID Ruta:", **form_style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_id_ruta = tk.Entry(form_detalle, **form_style_entry)
entry_id_ruta.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form_detalle, text="ID Modelo:", **form_style_label).grid(row=1, column=0, pady=5, sticky="w")
entry_id_modelo = tk.Entry(form_detalle, **form_style_entry)
entry_id_modelo.grid(row=1, column=1, pady=5, padx=10)

tk.Label(form_detalle, text="Consumo por Modelo:", **form_style_label).grid(row=2, column=0, pady=5, sticky="w")
entry_consumo_por_modelo = tk.Entry(form_detalle, **form_style_entry)
entry_consumo_por_modelo.grid(row=2, column=1, pady=5, padx=10)

tk.Button(
    frame_detalle,
    text="Guardar Detalle",
    command=insertar_detalle,
    **button_style
).pack(pady=15)





# =======================================
#          PESTAÑA DE ACTUALIZACIÓN
# =======================================

frame_actualizar = tk.Frame(notebook, bg="#f0ebe1")
notebook.add(frame_actualizar, text="♻ Actualizar Datos")

tabs_actualizar = ttk.Notebook(frame_actualizar)
tabs_actualizar.pack(fill="both", expand=True, padx=15, pady=15)

# ---------------------------------------
#  ESTILO GENERAL PARA FORMULARIOS
# ---------------------------------------

style_label = {
    "bg": "#faf7ef",
    "fg": "#4a3b22",
    "font": ("Segoe UI", 11, "bold"),
    "anchor": "w"
}

style_entry = {
    "font": ("Segoe UI", 11),
    "bd": 1
}

button_update = {
    "font": ("Segoe UI", 12, "bold"),
    "bg": "#1e64c8",
    "fg": "white",
    "activebackground": "#2d7af0",
    "relief": "flat",
    "cursor": "hand2",
    "width": 20,
    "height": 2
}


# ===================================================
#               --- ACTUALIZAR CONDUCTOR ---
# ===================================================

frame_act_conductor = tk.Frame(tabs_actualizar, bg="#faf7ef")
tabs_actualizar.add(frame_act_conductor, text="👤 Conductor")

tk.Label(
    frame_act_conductor,
    text="Actualizar Conductor",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form = tk.Frame(frame_act_conductor, bg="#faf7ef")
form.pack(pady=10)

tk.Label(form, text="ID Conductor:", **style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_id_conductor_act = tk.Entry(form, **style_entry)
entry_id_conductor_act.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form, text="Nuevo Nombre:", **style_label).grid(row=1, column=0, pady=5, sticky="w")
entry_nombre_conductor_act = tk.Entry(form, **style_entry)
entry_nombre_conductor_act.grid(row=1, column=1, pady=5, padx=10)

tk.Button(
    frame_act_conductor, text="Actualizar",
    command=actualizar_conductor, **button_update
).pack(pady=15)


# ===================================================
#               --- ACTUALIZAR MODELO ---
# ===================================================

frame_act_modelo = tk.Frame(tabs_actualizar, bg="#faf7ef")
tabs_actualizar.add(frame_act_modelo, text="📦 Modelo")

tk.Label(
    frame_act_modelo,
    text="Actualizar Modelo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form = tk.Frame(frame_act_modelo, bg="#faf7ef")
form.pack(pady=10)

tk.Label(form, text="ID Modelo:", **style_label).grid(row=0, column=0, pady=5, sticky="w")
entry_id_modelo_act = tk.Entry(form, **style_entry)
entry_id_modelo_act.grid(row=0, column=1, pady=5, padx=10)

tk.Label(form, text="Nueva Descripción:", **style_label).grid(row=1, column=0, pady=5, sticky="w")
entry_desc_modelo_act = tk.Entry(form, **style_entry)
entry_desc_modelo_act.grid(row=1, column=1, pady=5, padx=10)

tk.Button(
    frame_act_modelo, text="Actualizar",
    command=actualizar_modelo, **button_update
).pack(pady=15)


# ===================================================
#                  --- ACTUALIZAR RUTA ---
# ===================================================

frame_act_ruta = tk.Frame(tabs_actualizar, bg="#faf7ef")
tabs_actualizar.add(frame_act_ruta, text="🛣 Ruta")

tk.Label(
    frame_act_ruta,
    text="Actualizar Ruta",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form = tk.Frame(frame_act_ruta, bg="#faf7ef")
form.pack(pady=10)

labels_ruta = [
    ("ID Ruta:", "id_ruta_act"),
    ("Kilometraje:", "km_ruta_act"),
    ("Tipo de Ruta:", "tipo_ruta_act"),
    ("Descripción:", "desc_ruta_act"),
    ("Estado (0/1):", "estado_ruta_act")
]

entries_ruta = {}

for i, (label, key) in enumerate(labels_ruta):
    tk.Label(form, text=label, **style_label).grid(row=i, column=0, pady=5, sticky="w")
    entries_ruta[key] = tk.Entry(form, **style_entry)
    entries_ruta[key].grid(row=i, column=1, pady=5, padx=10)

entry_id_ruta_act       = entries_ruta["id_ruta_act"]
entry_km_ruta_act       = entries_ruta["km_ruta_act"]
entry_tipo_ruta_act     = entries_ruta["tipo_ruta_act"]
entry_desc_ruta_act     = entries_ruta["desc_ruta_act"]
entry_estado_ruta_act   = entries_ruta["estado_ruta_act"]

tk.Button(
    frame_act_ruta, text="Actualizar",
    command=actualizar_ruta, **button_update
).pack(pady=15)


# ===================================================
#               --- ACTUALIZAR VEHÍCULO ---
# ===================================================

frame_act_vehiculo = tk.Frame(tabs_actualizar, bg="#faf7ef")
tabs_actualizar.add(frame_act_vehiculo, text="🚗 Vehículo")

tk.Label(
    frame_act_vehiculo,
    text="Actualizar Vehículo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form = tk.Frame(frame_act_vehiculo, bg="#faf7ef")
form.pack(pady=10)

labels_veh = [
    ("Placa:", "placa_act"),
    ("Marca:", "marca_act"),
    ("Tonelaje:", "tonelaje_act"),
    ("ID Conductor:", "id_cond_act"),
    ("ID Modelo:", "id_modelo_act"),
    ("Centro de Costos:", "cc_act")
]

entries_veh = {}

for i, (label, key) in enumerate(labels_veh):
    tk.Label(form, text=label, **style_label).grid(row=i, column=0, pady=5, sticky="w")
    entries_veh[key] = tk.Entry(form, **style_entry)
    entries_veh[key].grid(row=i, column=1, pady=5, padx=10)

entry_placa_act        = entries_veh["placa_act"]
entry_marca_act        = entries_veh["marca_act"]
entry_tonelaje_act     = entries_veh["tonelaje_act"]
entry_conductor_act    = entries_veh["id_cond_act"]
entry_modelo_act       = entries_veh["id_modelo_act"]
entry_cc_act           = entries_veh["cc_act"]

tk.Button(
    frame_act_vehiculo, text="Actualizar",
    command=actualizar_vehiculo, **button_update
).pack(pady=15)


# ===================================================
#               --- ACTUALIZAR DETALLE ---
# ===================================================

frame_act_detalle = tk.Frame(tabs_actualizar, bg="#faf7ef")
tabs_actualizar.add(frame_act_detalle, text="📑 Detalle")

tk.Label(
    frame_act_detalle,
    text="Actualizar Detalle",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

form = tk.Frame(frame_act_detalle, bg="#faf7ef")
form.pack(pady=10)

labels_det = [
    ("ID Detalle:", "id_detalle_act"),
    ("ID Ruta:", "id_ruta_det_act"),
    ("ID Modelo:", "id_modelo_det_act"),
    ("Consumo por Modelo:", "consumo_det_act")
]

entries_det = {}

for i, (label, key) in enumerate(labels_det):
    tk.Label(form, text=label, **style_label).grid(row=i, column=0, pady=5, sticky="w")
    entries_det[key] = tk.Entry(form, **style_entry)
    entries_det[key].grid(row=i, column=1, pady=5, padx=10)

entry_id_detalle_act      = entries_det["id_detalle_act"]
entry_id_ruta_det_act     = entries_det["id_ruta_det_act"]
entry_id_modelo_det_act   = entries_det["id_modelo_det_act"]
entry_consumo_det_act     = entries_det["consumo_det_act"]

tk.Button(
    frame_act_detalle, text="Actualizar",
    command=actualizar_detalle, **button_update
).pack(pady=15)

# =======================================
#          PESTAÑA DE ELIMINACIÓN
# =======================================

frame_eliminar = tk.Frame(notebook, bg="#f0ebe1")
notebook.add(frame_eliminar, text="🗑 Eliminar Datos")

tabs_eliminar = ttk.Notebook(frame_eliminar)
tabs_eliminar.pack(fill="both", expand=True, padx=15, pady=15)

# ---------------------------------------
#  ESTILO GENERAL
# ---------------------------------------

delete_label_style = {
    "bg": "#faf7ef",
    "fg": "#4a3b22",
    "font": ("Segoe UI", 11, "bold"),
    "anchor": "w"
}

delete_entry_style = {
    "font": ("Segoe UI", 11),
    "bd": 1
}

button_delete_style = {
    "font": ("Segoe UI", 12, "bold"),
    "bg": "#c62828",
    "fg": "white",
    "activebackground": "#e53935",
    "relief": "flat",
    "cursor": "hand2",
    "width": 20,
    "height": 2
}


# ===================================================
#               --- ELIMINAR CONDUCTOR ---
# ===================================================

frame_del_conductor = tk.Frame(tabs_eliminar, bg="#faf7ef")
tabs_eliminar.add(frame_del_conductor, text="👤 Conductor")

tk.Label(
    frame_del_conductor,
    text="Eliminar Conductor",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

frm = tk.Frame(frame_del_conductor, bg="#faf7ef")
frm.pack(pady=10)

tk.Label(frm, text="ID Conductor:", **delete_label_style).grid(row=0, column=0, sticky="w", pady=5)
entry_id_conductor_del = tk.Entry(frm, **delete_entry_style)
entry_id_conductor_del.grid(row=0, column=1, padx=10, pady=5)

tk.Button(
    frame_del_conductor,
    text="Eliminar Conductor",
    command=eliminar_conductor,
    **button_delete_style
).pack(pady=15)


# ===================================================
#               --- ELIMINAR MODELO ---
# ===================================================

frame_del_modelo = tk.Frame(tabs_eliminar, bg="#faf7ef")
tabs_eliminar.add(frame_del_modelo, text="📦 Modelo")

tk.Label(
    frame_del_modelo,
    text="Eliminar Modelo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

frm = tk.Frame(frame_del_modelo, bg="#faf7ef")
frm.pack(pady=10)

tk.Label(frm, text="ID Modelo:", **delete_label_style).grid(row=0, column=0, sticky="w", pady=5)
entry_id_modelo_del = tk.Entry(frm, **delete_entry_style)
entry_id_modelo_del.grid(row=0, column=1, padx=10, pady=5)

tk.Button(
    frame_del_modelo,
    text="Eliminar Modelo",
    command=eliminar_modelo,
    **button_delete_style
).pack(pady=15)


# ===================================================
#               --- ELIMINAR RUTA ---
# ===================================================

frame_del_ruta = tk.Frame(tabs_eliminar, bg="#faf7ef")
tabs_eliminar.add(frame_del_ruta, text="🛣 Ruta")

tk.Label(
    frame_del_ruta,
    text="Eliminar Ruta",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

frm = tk.Frame(frame_del_ruta, bg="#faf7ef")
frm.pack(pady=10)

tk.Label(frm, text="ID Ruta:", **delete_label_style).grid(row=0, column=0, pady=5, sticky="w")
entry_id_ruta_del = tk.Entry(frm, **delete_entry_style)
entry_id_ruta_del.grid(row=0, column=1, pady=5, padx=10)

tk.Button(
    frame_del_ruta,
    text="Eliminar Ruta",
    command=eliminar_ruta,
    **button_delete_style
).pack(pady=15)


# ===================================================
#               --- ELIMINAR VEHÍCULO ---
# ===================================================

frame_del_vehiculo = tk.Frame(tabs_eliminar, bg="#faf7ef")
tabs_eliminar.add(frame_del_vehiculo, text="🚗 Vehículo")

tk.Label(
    frame_del_vehiculo,
    text="Eliminar Vehículo",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

frm = tk.Frame(frame_del_vehiculo, bg="#faf7ef")
frm.pack(pady=10)

tk.Label(frm, text="Placa:", **delete_label_style).grid(row=0, column=0, pady=5, sticky="w")
entry_placa_del = tk.Entry(frm, **delete_entry_style)
entry_placa_del.grid(row=0, column=1, pady=5, padx=10)

tk.Button(
    frame_del_vehiculo,
    text="Eliminar Vehículo",
    command=eliminar_vehiculo,
    **button_delete_style
).pack(pady=15)


# ===================================================
#               --- ELIMINAR DETALLE ---
# ===================================================

frame_del_detalle = tk.Frame(tabs_eliminar, bg="#faf7ef")
tabs_eliminar.add(frame_del_detalle, text="📑 Detalle")

tk.Label(
    frame_del_detalle,
    text="Eliminar Detalle",
    bg="#faf7ef",
    fg="#3d2f1c",
    font=("Segoe UI", 20, "bold")
).pack(pady=25)

frm = tk.Frame(frame_del_detalle, bg="#faf7ef")
frm.pack(pady=10)

tk.Label(frm, text="ID Detalle:", **delete_label_style).grid(row=0, column=0, pady=5, sticky="w")
entry_id_detalle_del = tk.Entry(frm, **delete_entry_style)
entry_id_detalle_del.grid(row=0, column=1, pady=5, padx=10)

tk.Button(
    frame_del_detalle,
    text="Eliminar Detalle",
    command=eliminar_detalle,
    **button_delete_style
).pack(pady=15)



# Ejecutar ventana
ventana.mainloop()
