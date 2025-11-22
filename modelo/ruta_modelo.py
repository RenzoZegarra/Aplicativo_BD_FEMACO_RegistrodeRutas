from .conexion import ConexionDB

class RutaModelo:
    def __init__(self, db: ConexionDB = None):
        # Inicializa el modelo con una instancia de la conexión a la base de datos.
        # Si no se pasa una conexión, se crea una nueva.
        self.db = db or ConexionDB()

    def insertar_ruta(self, kilometraje, tipo, descripcion, estado):
        # Inserta una nueva ruta en la base de datos usando un procedimiento almacenado.
        # Se convierten a entero los valores numéricos antes de enviarlos.
        self.db.ejecutar_procedimiento(
            'insertar_ruta',
            (int(kilometraje), tipo, descripcion, int(estado))
        )
        # Confirma los cambios realizados en la base de datos.
        self.db.commit()

    def actualizar_ruta(self, id_ruta, kilometraje, tipo, descripcion, estado):
        # Actualiza una ruta existente identificada por su id.
        self.db.ejecutar_procedimiento(
            'actualizar_ruta',
            (int(id_ruta), int(kilometraje), tipo, descripcion, int(estado))
        )
        # Guarda los cambios.
        self.db.commit()

    def eliminar_ruta(self, id_ruta):
        # Elimina una ruta de la base de datos según el id proporcionado.
        self.db.ejecutar_procedimiento('sp_eliminar_ruta', (id_ruta,))
        # Aplica la eliminación.
        self.db.commit()

    def listar_rutas(self):
        # Retorna una lista con todas las rutas disponibles.
        # fetch=True indica que deben devolverse los resultados del procedimiento.
        return self.db.ejecutar_procedimiento('mostrar_todas_rutas', (), fetch=True)

    # -------------------------------
    # Consultas específicas (reportes)
    # -------------------------------

    def consulta_vehiculos_con_conductor(self):
        # Consulta vehículos junto con su conductor asignado.
        return self.db.ejecutar_procedimiento('consulta1_vehiculos_con_conductor', (), fetch=True)

    def consulta_rutas_activas(self):
        # Devuelve únicamente las rutas en estado activo.
        return self.db.ejecutar_procedimiento('consulta2_rutas_activas', (), fetch=True)

    def consulta_detalles_rutas(self):
        # Obtiene detalles extendidos de las rutas.
        return self.db.ejecutar_procedimiento('consulta3_rutas_detalles', (), fetch=True)

    def consulta_top_rendimiento(self):
        # Consulta un ranking o listado de rutas/vehículos con mayor rendimiento.
        return self.db.ejecutar_procedimiento('consulta4_top_rendimiento', (), fetch=True)

    def consulta_vehiculos_modelo(self):
        # Consulta los vehículos agrupados o filtrados por modelo.
        return self.db.ejecutar_procedimiento('consulta5_vehiculos_modelo', (), fetch=True)

    def consulta_modelos_usados(self):
        # Devuelve los modelos de vehículos más utilizados o más frecuentes.
        return self.db.ejecutar_procedimiento('consulta6_modelos_usados', (), fetch=True)

    def consulta_consumo_promedio(self):
        # Consulta el consumo promedio por modelo o tipo de vehículo.
        return self.db.ejecutar_procedimiento('consulta7_consumo_promedio_modelo', (), fetch=True)

    def consulta_vehiculos_pesados(self):
        # Devuelve vehículos con tonelaje mayor a cierto umbral (vehículos pesados).
        return self.db.ejecutar_procedimiento('consulta8_vehiculos_tonelaje', (), fetch=True)

    def consulta_rutas_tipo(self):
        # Consulta las rutas según el tipo (urbana, rural, etc.).
        return self.db.ejecutar_procedimiento('consulta9_rutas_tipo', (), fetch=True)

    def consulta_rutas_inactivas(self):
        # Devuelve únicamente las rutas que están inactivas.
        return self.db.ejecutar_procedimiento('consulta10_rutas_inactivas', (), fetch=True)
