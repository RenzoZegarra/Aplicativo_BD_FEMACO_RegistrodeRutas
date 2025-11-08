import mysql.connector

conexion = mysql.connector.connect(user='root', password='root',
                                   host='localhost',
                                   database='femaco_registro_de_rutas',
                                   port='3306')
print(conexion)
if conexion.is_connected():
    print("SE CONECTO CORRECTAMENTE A LA BASE DE DATOS")

#Ejecución de consulta
cursor=conexion.cursor()
cursor.execute("SELECT * FROM conductor")

#Obtener datos
for fila in cursor.fetchall():
    print(fila)

#Cerrar conexión
cursor.close()
conexion.close()