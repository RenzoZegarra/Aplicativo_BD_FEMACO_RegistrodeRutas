from modelo.vehiculo_modelo import VehiculoModelo
from modelo.conexion import ConexionDB

class VehiculoController:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el controlador con una conexión a la base de datos.
        # Si no se pasa una conexión, se crea una nueva.
        # El modelo VehiculoModelo utiliza esta conexión para ejecutar sus operaciones.
        self.db = db or ConexionDB()
        self.model = VehiculoModelo(self.db)

    def agregar(self, placa, id_conductor, id_modelo, marca, tonelaje, centro_costos):
        # Llama al modelo para insertar un nuevo vehículo en la base de datos.
        # Todos los parámetros se envían directamente al procedimiento almacenado.
        return self.model.insertar_vehiculo(
            placa, id_conductor, id_modelo, marca, tonelaje, centro_costos
        )

    def actualizar(self, placa, id_conductor, id_modelo, marca, tonelaje, centro_costos):
        # Llama al modelo para actualizar los datos de un vehículo existente.
        return self.model.actualizar_vehiculo(
            placa, id_conductor, id_modelo, marca, tonelaje, centro_costos
        )

    def eliminar(self, placa):
        # Llama al modelo para eliminar un vehículo según su placa.
        return self.model.eliminar_vehiculo(placa)

    def listar(self):
        # Recupera y retorna la lista completa de vehículos registrados.
        return self.model.listar_vehiculos()
