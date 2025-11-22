from .conexion import ConexionDB

class ModeloModelo:
    def __init__(self, db: ConexionDB = None):
        # Inicializa la clase con una conexión a la base de datos.
        # Si no se proporciona una conexión externa, se crea una nueva.
        self.db = db or ConexionDB()

    def insertar_modelo(self, descripcion):
        # Inserta un nuevo modelo en la base de datos utilizando un procedimiento almacenado.
        # Se envía únicamente la descripción del modelo.
        self.db.ejecutar_procedimiento('insertar_modelo', (descripcion,))
        # Confirma los cambios en la base de datos.
        self.db.commit()

    def actualizar_modelo(self, id_modelo, descripcion):
        # Actualiza un modelo existente identificado por su ID.
        # id_modelo se convierte a entero para asegurar el tipo correcto.
        self.db.ejecutar_procedimiento(
            'actualizar_modelo',
            (int(id_modelo), descripcion)
        )
        # Guarda los cambios realizados.
        self.db.commit()

    def eliminar_modelo(self, id_modelo):
        # Elimina un modelo según su ID utilizando el procedimiento almacenado respectivo.
        self.db.ejecutar_procedimiento('sp_eliminar_modelo', (id_modelo,))
        # Aplica la eliminación en la base de datos.
        self.db.commit()

    def listar_modelos(self):
        # Recupera y retorna todos los modelos registrados en la base de datos.
        # fetch=True indica que deben devolverse los resultados.
        return self.db.ejecutar_procedimiento('mostrar_todos_modelos', (), fetch=True)
