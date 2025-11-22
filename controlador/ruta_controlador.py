from modelo.ruta_modelo import RutaModelo
from modelo.conexion import ConexionDB

class RutaController:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el controlador con una conexión a la base de datos.
        # Si no se pasa una conexión, se crea una nueva.
        # El modelo RutaModelo utiliza esta misma conexión para ejecutar sus operaciones.
        self.db = db or ConexionDB()
        self.model = RutaModelo(self.db)

    def agregar(self, kilometraje, tipo, descripcion, estado):
        # Llama al modelo para insertar una nueva ruta en la base de datos.
        return self.model.insertar_ruta(kilometraje, tipo, descripcion, estado)

    def actualizar(self, id_ruta, kilometraje, tipo, descripcion, estado):
        # Llama al modelo para actualizar los datos de una ruta identificada por su ID.
        return self.model.actualizar_ruta(id_ruta, kilometraje, tipo, descripcion, estado)

    def eliminar(self, id_ruta):
        # Llama al modelo para eliminar una ruta según su ID.
        return self.model.eliminar_ruta(id_ruta)

    def listar(self):
        # Recupera y retorna todas las rutas almacenadas en la base de datos.
        return self.model.listar_rutas()

    # --------------------------------------------------
    # Wrappers para consultas especiales / reportes
    # --------------------------------------------------

    def consulta_vehiculos_con_conductor(self):
        # Devuelve vehículos junto con el conductor asignado.
        return self.model.consulta_vehiculos_con_conductor()

    def consulta_rutas_activas(self):
        # Devuelve únicamente las rutas que están activas.
        return self.model.consulta_rutas_activas()

    def consulta_detalles_rutas(self):
        # Retorna detalles completos o enriquecidos de rutas.
        return self.model.consulta_detalles_rutas()

    def consulta_top_rendimiento(self):
        # Devuelve un ranking o lista de rutas/vehículos con mejor rendimiento.
        return self.model.consulta_top_rendimiento()

    def consulta_vehiculos_modelo(self):
        # Devuelve vehículos agrupados o filtrados según su modelo.
        return self.model.consulta_vehiculos_modelo()

    def consulta_modelos_usados(self):
        # Muestra modelos de vehículos que han sido utilizados en rutas.
        return self.model.consulta_modelos_usados()

    def consulta_consumo_promedio(self):
        # Devuelve el consumo promedio por modelo o ruta.
        return self.model.consulta_consumo_promedio()

    def consulta_vehiculos_pesados(self):
        # Retorna vehículos clasificados como pesados (según su tonelaje).
        return self.model.consulta_vehiculos_pesados()

    def consulta_rutas_tipo(self):
        # Devuelve rutas filtradas según su tipo (urbana, rural, etc.).
        return self.model.consulta_rutas_tipo()

    def consulta_rutas_inactivas(self):
        # Devuelve rutas que están marcadas como inactivas.
        return self.model.consulta_rutas_inactivas()
