from .conexion import ConexionDB

class VehiculoModelo:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el modelo con una instancia de la conexión a la base de datos.
        # Si no se proporciona una conexión, crea una nueva.
        self.db = db or ConexionDB()

    def insertar_vehiculo(self, placa, id_conductor, id_modelo, marca, tonelaje, centro_costos):
        # Inserta un nuevo vehículo en la base de datos usando un procedimiento almacenado.
        # Se convierten a entero los valores que deben ser numéricos.
        self.db.ejecutar_procedimiento(
            'insertar_vehiculo',
            (placa, int(id_conductor), int(id_modelo), marca, int(tonelaje), centro_costos)
        )
        # Confirma los cambios en la base de datos.
        self.db.commit()

    def actualizar_vehiculo(self, placa, id_conductor, id_modelo, marca, tonelaje, centro_costos):
        # Actualiza la información de un vehículo existente mediante un procedimiento almacenado.
        self.db.ejecutar_procedimiento(
            'actualizar_vehiculo',
            (placa, int(id_conductor), int(id_modelo), marca, int(tonelaje), centro_costos)
        )
        # Guarda los cambios.
        self.db.commit()

    def eliminar_vehiculo(self, placa):
        # Elimina un vehículo de la base de datos según la placa indicada.
        self.db.ejecutar_procedimiento('sp_eliminar_vehiculo', (placa,))
        # Se confirma la eliminación.
        self.db.commit()

    def listar_vehiculos(self):
        # Obtiene y devuelve la lista de todos los vehículos registrados.
        # fetch=True indica que se deben recuperar los resultados del procedimiento.
        return self.db.ejecutar_procedimiento('mostrar_todos_vehiculos', (), fetch=True)
