from .conexion import ConexionDB

class ConductorModelo:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el modelo con una instancia de conexión a la base de datos.
        # Si no se proporciona una conexión externa, se crea una nueva.
        # No se conecta automáticamente; la vista/controlador decide cuándo llamar a conectar().
        self.db = db or ConexionDB()

    def insertar_conductor(self, nombre):
        # Inserta un nuevo conductor en la base de datos usando un procedimiento almacenado.
        # El único parámetro requerido es el nombre del conductor.
        self.db.ejecutar_procedimiento('insertar_conductor', (nombre,))
        # Confirma los cambios tras la inserción.
        self.db.commit()

    def actualizar_conductor(self, id_conductor, nuevo_nombre):
        # Actualiza los datos de un conductor existente, identificado por su ID.
        # Se asegura que el ID sea un entero antes de enviarlo al procedimiento.
        self.db.ejecutar_procedimiento(
            'actualizar_conductor',
            (int(id_conductor), nuevo_nombre)
        )
        # Guarda los cambios realizados.
        self.db.commit()

    def eliminar_conductor(self, id_conductor):
        # Elimina un conductor de la base de datos utilizando su ID.
        self.db.ejecutar_procedimiento('sp_eliminar_conductor', (id_conductor,))
        # Aplica la eliminación en la base de datos.
        self.db.commit()

    def listar_conductores(self):
        # Recupera y retorna la lista completa de conductores registrados.
        # fetch=True indica que deben devolverse los resultados.
        return self.db.ejecutar_procedimiento('mostrar_todos_conductores', (), fetch=True)
