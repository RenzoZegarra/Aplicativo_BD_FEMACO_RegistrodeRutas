from modelo.detalle_modelo import DetalleModelo
from modelo.conexion import ConexionDB

class DetalleController:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el controlador con una conexión a la base de datos.
        # Si no se proporciona una conexión externa, se crea una nueva.
        # El modelo DetalleModelo utiliza esta misma conexión para operar.
        self.db = db or ConexionDB()
        self.model = DetalleModelo(self.db)

    def agregar(self, id_ruta, id_modelo, consumo):
        # Llama al modelo para insertar un nuevo detalle (relación ruta-modelo-consumo).
        return self.model.insertar_detalle(id_ruta, id_modelo, consumo)

    def actualizar(self, id_detalle, id_ruta, id_modelo, consumo):
        # Llama al modelo para actualizar un detalle existente, identificado por su ID.
        return self.model.actualizar_detalle(id_detalle, id_ruta, id_modelo, consumo)

    def eliminar(self, id_detalle):
        # Llama al modelo para eliminar un detalle según su ID.
        return self.model.eliminar_detalle(id_detalle)

    def listar(self):
        # Recupera todos los detalles almacenados en la base de datos.
        return self.model.listar_detalles()
