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
        nombre = input("Ingrese el nombre del conductor: ")
        licencia = input("Ingrese el número de licencia: ")
        telefono = input("Ingrese el teléfono: ")

        sql = "INSERT INTO conductor (nombre, licencia, telefono) VALUES (%s, %s, %s)"
        datos = (nombre, licencia, telefono)
        cursor.execute(sql, datos)
        conexion.commit()
        print("Conductor agregado correctamente.")
    except Error as e:
        print("Error al agregar conductor:", e)
    finally:
        cursor.close()
        conexion.close()

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

def menu():
    """Menú principal de opciones."""
    while True:
        print("\n=== MENÚ DE CONDUCTORES ===")
        print("1. Mostrar todos los conductores")
        print("2. Agregar nuevo conductor")
        print("3. Eliminar conductor")
        print("4. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_conductores()
        elif opcion == "2":
            agregar_conductor()
        elif opcion == "3":
            eliminar_conductor()
        elif opcion == "4":
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")

if __name__ == "__main__":
    menu()
