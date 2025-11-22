from modelo.modelo_modelo import ModeloModelo
from modelo.conexion import ConexionDB

class ModeloController:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el controlador con una instancia compartida de la base de datos.
        # Si no se pasa una conexión, se crea una nueva.
        # El modelo ModeloModelo utiliza esta misma conexión para ejecutar sus operaciones.
        self.db = db or ConexionDB()
        self.model = ModeloModelo(self.db)

    def agregar(self, descripcion):
        # Llama al modelo para insertar un nuevo modelo de vehículo.
        return self.model.insertar_modelo(descripcion)

    def actualizar(self, id_modelo, descripcion):
        # Llama al modelo para actualizar un modelo existente según su ID.
        return self.model.actualizar_modelo(id_modelo, descripcion)

    def eliminar(self, id_modelo):
        # Llama al modelo para eliminar un modelo específico de la base de datos.
        return self.model.eliminar_modelo(id_modelo)

    def listar(self):
        # Recupera y retorna la lista completa de modelos registrados.
        return self.model.listar_modelos()
