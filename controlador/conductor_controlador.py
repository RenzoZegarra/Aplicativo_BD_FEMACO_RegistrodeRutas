from modelo.conductor_modelo import ConductorModelo
from modelo.conexion import ConexionDB

class ConductorController:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el controlador con una instancia compartida de la base de datos.
        # Si no se proporciona una conexión, crea una nueva.
        # También inicializa el modelo del conductor utilizando esa misma conexión.
        self.db = db or ConexionDB()
        self.model = ConductorModelo(self.db)

    def conectar(self):
        # Intenta establecer la conexión a la base de datos.
        # Devuelve True si la conexión fue exitosa.
        return self.db.conectar()

    def cerrar(self):
        # Cierra el cursor y la conexión a la base de datos.
        return self.db.cerrar()

    def agregar(self, nombre):
        # Llama al modelo para insertar un nuevo conductor.
        return self.model.insertar_conductor(nombre)

    def actualizar(self, id_conductor, nuevo_nombre):
        # Llama al modelo para actualizar un conductor existente.
        return self.model.actualizar_conductor(id_conductor, nuevo_nombre)

    def eliminar(self, id_conductor):
        # Llama al modelo para eliminar un conductor según su ID.
        return self.model.eliminar_conductor(id_conductor)

    def listar(self):
        # Llama al modelo para obtener la lista completa de conductores.
        return self.model.listar_conductores()
