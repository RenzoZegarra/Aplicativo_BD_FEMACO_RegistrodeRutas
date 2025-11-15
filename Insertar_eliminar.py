import mysql.connector
from mysql.connector import Error

def conectar_bd():
    """Conecta a la base de datos y retorna la conexión y el cursor."""
    conexion = mysql.connector.connect(
        user='root',
        password='root',
        host='localhost',
        database='femaco_registro_de_rutas',
        port='3306'
    )
    return conexion, conexion.cursor()

def mostrar_conductores():
    """Muestra todos los conductores en la tabla."""
    try:
        conexion, cursor = conectar_bd()
        cursor.execute("SELECT * FROM conductor")
        registros = cursor.fetchall()
        print("\n=== LISTA DE CONDUCTORES ===")
        for fila in registros:
            print(fila)
    except Error as e:
        print("Error al obtener los conductores:", e)
    finally:
        cursor.close()
        conexion.close()

def agregar_conductor():
    """Permite agregar un nuevo conductor."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== AGREGAR NUEVO CONDUCTOR ===")
        nombre = input("Ingrese el nombre completo del conductor: ")

        sql = "INSERT INTO Conductor (Nombre_Conductor) VALUES (%s)"
        datos = (nombre,)
        cursor.execute(sql, datos)
        conexion.commit()
        print("Conductor agregado correctamente.")
    except Error as e:
        print("Error al agregar conductor:", e)
    finally:
        cursor.close()
        conexion.close()

#ELIMINAR

def eliminar_conductor():
    """Permite eliminar un conductor por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ELIMINAR CONDUCTOR ===")
        id_conductor = input("Ingrese el ID del conductor a eliminar: ")

        sql = "DELETE FROM conductor WHERE id_conductor = %s"
        cursor.execute(sql, (id_conductor,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Conductor eliminado correctamente.")
        else:
            print("No se encontró un conductor con ese ID.")
    except Error as e:
        print("Error al eliminar conductor:", e)
    finally:
        cursor.close()
        conexion.close()

def eliminar_detalle():
    """Permite eliminar un registro de Detalle por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ELIMINAR DETALLE ===")
        id_detalle = input("Ingrese el ID del detalle a eliminar: ").strip()

        sql = "DELETE FROM Detalle WHERE id_detalle = %s"
        cursor.execute(sql, (id_detalle,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Detalle eliminado correctamente.")
        else:
            print("No se encontró un detalle con ese ID.")
    except Error as e:
        print("Error al eliminar detalle:", e)
    finally:
        cursor.close()
        conexion.close()

def eliminar_ruta():
    """Permite eliminar una ruta por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ELIMINAR RUTA ===")
        id_ruta = input("Ingrese el ID de la ruta a eliminar: ").strip()

        sql = "DELETE FROM Ruta WHERE id_ruta = %s"
        cursor.execute(sql, (id_ruta,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Ruta eliminada correctamente.")
        else:
            print("No se encontró una ruta con ese ID.")
    except Error as e:
        print("Error al eliminar ruta:", e)
    finally:
        cursor.close()
        conexion.close()

def eliminar_modelo():
    """Permite eliminar un modelo por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ELIMINAR MODELO ===")
        id_modelo = input("Ingrese el ID del modelo a eliminar: ").strip()

        sql = "DELETE FROM Modelo WHERE id_modelo = %s"
        cursor.execute(sql, (id_modelo,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Modelo eliminado correctamente.")
        else:
            print("No se encontró un modelo con ese ID.")
    except Error as e:
        print("Error al eliminar modelo:", e)
    finally:
        cursor.close()
        conexion.close()

def eliminar_vehiculo():
    """Permite eliminar un vehículo por su placa."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ELIMINAR VEHÍCULO ===")
        placa = input("Ingrese la placa del vehículo a eliminar: ").strip()

        sql = "DELETE FROM Vehiculo WHERE placa = %s"
        cursor.execute(sql, (placa,))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Vehículo eliminado correctamente.")
        else:
            print("No se encontró un vehículo con esa placa.")
    except Error as e:
        print("Error al eliminar vehículo:", e)
    finally:
        cursor.close()
        conexion.close()

#UPDATE

def actualizar_modelo():
    """Permite modificar la descripción de un modelo por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ACTUALIZAR MODELO ===")

        id_modelo = input("Ingrese el ID del modelo que desea actualizar: ").strip()
        nueva_descripcion = input("Ingrese la nueva descripción del modelo: ").strip()

        sql = "UPDATE Modelo SET modelo_descripcion = %s WHERE id_modelo = %s"
        cursor.execute(sql, (nueva_descripcion, id_modelo))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Modelo actualizado correctamente.")
        else:
            print("No se encontró un modelo con ese ID.")
    except Error as e:
        print("Error al actualizar modelo:", e)
    finally:
        cursor.close()
        conexion.close()

def actualizar_vehiculo():
    """Permite actualizar los datos de un vehículo usando su placa."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ACTUALIZAR VEHÍCULO ===")

        placa = input("Ingrese la placa del vehículo a actualizar: ").strip()

        print("¿Qué desea modificar?")
        print("1. Marca")
        print("2. Tonelaje")
        print("3. Centro de costos")
        print("4. ID del conductor")
        print("5. ID del modelo")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo = input("Nueva marca: ").strip()
            sql = "UPDATE Vehiculo SET marca = %s WHERE placa = %s"

        elif opcion == "2":
            nuevo = input("Nuevo tonelaje: ").strip()
            sql = "UPDATE Vehiculo SET tonelaje = %s WHERE placa = %s"

        elif opcion == "3":
            nuevo = input("Nuevo centro de costos: ").strip()
            sql = "UPDATE Vehiculo SET centro_costos = %s WHERE placa = %s"

        elif opcion == "4":
            nuevo = input("Nuevo ID de conductor: ").strip()
            sql = "UPDATE Vehiculo SET id_conductor = %s WHERE placa = %s"

        elif opcion == "5":
            nuevo = input("Nuevo ID de modelo: ").strip()
            sql = "UPDATE Vehiculo SET id_modelo = %s WHERE placa = %s"

        else:
            print("Opción no válida.")
            return

        cursor.execute(sql, (nuevo, placa))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Vehículo actualizado correctamente.")
        else:
            print("No se encontró un vehículo con esa placa.")
    except Error as e:
        print("Error al actualizar vehículo:", e)
    finally:
        cursor.close()
        conexion.close()

def actualizar_ruta():
    """Permite modificar los datos de una ruta por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ACTUALIZAR RUTA ===")

        id_ruta = input("Ingrese el ID de la ruta a actualizar: ").strip()

        print("¿Qué desea modificar?")
        print("1. Kilometraje")
        print("2. Tipo de ruta")
        print("3. Descripción")
        print("4. Estado de la ruta (1=activo, 0=inactivo)")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo = input("Nuevo kilometraje: ").strip()
            sql = "UPDATE Ruta SET kilometraje = %s WHERE id_ruta = %s"

        elif opcion == "2":
            nuevo = input("Nuevo tipo de ruta: ").strip()
            sql = "UPDATE Ruta SET tipo_ruta = %s WHERE id_ruta = %s"

        elif opcion == "3":
            nuevo = input("Nueva descripción: ").strip()
            sql = "UPDATE Ruta SET descripcion = %s WHERE id_ruta = %s"

        elif opcion == "4":
            nuevo = input("Nuevo estado (1 o 0): ").strip()
            sql = "UPDATE Ruta SET estado_ruta = %s WHERE id_ruta = %s"

        else:
            print("Opción inválida.")
            return

        cursor.execute(sql, (nuevo, id_ruta))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Ruta actualizada correctamente.")
        else:
            print("No se encontró una ruta con ese ID.")
    except Error as e:
        print("Error al actualizar ruta:", e)
    finally:
        cursor.close()
        conexion.close()

def actualizar_detalle():
    """Permite actualizar un registro de Detalle por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ACTUALIZAR DETALLE ===")
        id_detalle = input("Ingrese el ID del detalle a actualizar: ").strip()

        print("¿Qué desea modificar?")
        print("1. ID de ruta")
        print("2. ID de modelo")
        print("3. Consumo por modelo")
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            nuevo = input("Nuevo ID de ruta: ").strip()
            sql = "UPDATE Detalle SET id_ruta = %s WHERE id_detalle = %s"

        elif opcion == "2":
            nuevo = input("Nuevo ID de modelo: ").strip()
            sql = "UPDATE Detalle SET id_modelo = %s WHERE id_detalle = %s"

        elif opcion == "3":
            nuevo = input("Nuevo consumo por modelo: ").strip()
            sql = "UPDATE Detalle SET consumo_por_modelo = %s WHERE id_detalle = %s"

        else:
            print("Opción inválida.")
            return

        cursor.execute(sql, (nuevo, id_detalle))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Detalle actualizado correctamente.")
        else:
            print("No se encontró un detalle con ese ID.")
    except Error as e:
        print("Error al actualizar detalle:", e)
    finally:
        cursor.close()
        conexion.close()

def actualizar_conductor():
    """Permite actualizar el nombre de un conductor por su ID."""
    try:
        conexion, cursor = conectar_bd()
        print("\n=== ACTUALIZAR CONDUCTOR ===")
        id_conductor = input("Ingrese el ID del conductor a actualizar: ").strip()
        nuevo_nombre = input("Ingrese el nuevo nombre del conductor: ").strip()

        sql = "UPDATE Conductor SET nombre_conductor = %s WHERE id_conductor = %s"
        cursor.execute(sql, (nuevo_nombre, id_conductor))
        conexion.commit()

        if cursor.rowcount > 0:
            print("Conductor actualizado correctamente.")
        else:
            print("No se encontró un conductor con ese ID.")
    except Error as e:
        print("Error al actualizar conductor:", e)
    finally:
        cursor.close()
        conexion.close()



def menu():
    """Menú principal general."""
    while True:
        print("\n========= MENÚ PRINCIPAL =========")
        print("1. Gestión de Conductores")
        print("2. Gestión de Vehículos")
        print("3. Gestión de Modelos")
        print("4. Gestión de Rutas")
        print("5. Gestión de Detalles")
        print("0. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_conductores()
        elif opcion == "2":
            menu_vehiculos()
        elif opcion == "3":
            menu_modelos()
        elif opcion == "4":
            menu_rutas()
        elif opcion == "5":
            menu_detalles()
        elif opcion == "0":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")


# =======================
# SUBMENÚ DE CONDUCTORES
# =======================
def menu_conductores():
    while True:
        print("\n=== MENÚ DE CONDUCTORES ===")
        print("1. Mostrar todos los conductores")
        print("2. Agregar nuevo conductor")
        print("3. Actualizar conductor")
        print("4. Eliminar conductor")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_conductores()
        elif opcion == "2":
            agregar_conductor()
        elif opcion == "3":
            actualizar_conductor()
        elif opcion == "4":
            eliminar_conductor()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# ===================
# SUBMENÚ VEHÍCULOS
# ===================
def menu_vehiculos():
    while True:
        print("\n=== MENÚ DE VEHÍCULOS ===")
        print("1. Actualizar vehículo")
        print("2. Eliminar vehículo")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            actualizar_vehiculo()
        elif opcion == "2":
            eliminar_vehiculo()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# =================
# SUBMENÚ MODELOS
# =================
def menu_modelos():
    while True:
        print("\n=== MENÚ DE MODELOS ===")
        print("1. Actualizar modelo")
        print("2. Eliminar modelo")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            actualizar_modelo()
        elif opcion == "2":
            eliminar_modelo()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# ===============
# SUBMENÚ RUTAS
# ===============
def menu_rutas():
    while True:
        print("\n=== MENÚ DE RUTAS ===")
        print("1. Actualizar ruta")
        print("2. Eliminar ruta")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            actualizar_ruta()
        elif opcion == "2":
            eliminar_ruta()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# ======================
# SUBMENÚ DETALLES (DETALLE)
# ======================
def menu_detalles():
    while True:
        print("\n=== MENÚ DE DETALLES ===")
        print("1. Actualizar detalle")
        print("2. Eliminar detalle")
        print("0. Volver")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            actualizar_detalle()
        elif opcion == "2":
            eliminar_detalle()
        elif opcion == "0":
            break
        else:
            print("Opción inválida.")


# =======================
# EJECUCIÓN DEL PROGRAMA
# =======================
if __name__ == "__main__":
    menu()
