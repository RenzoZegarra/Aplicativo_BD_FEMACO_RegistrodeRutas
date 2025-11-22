from .conexion import ConexionDB

class DetalleModelo:
    def __init__(self, db: ConexionDB = None):
        # Inicializa la clase con una conexión a la base de datos.
        # Si no se proporciona una conexión externa, se crea una nueva.
        self.db = db or ConexionDB()

    def insertar_detalle(self, id_ruta, id_modelo, consumo):
        # Inserta un nuevo detalle relacionado con una ruta y un modelo.
        # Se convierte cada parámetro a su tipo correspondiente antes de enviarlo.
        self.db.ejecutar_procedimiento(
            'insertar_detalle',
            (int(id_ruta), int(id_modelo), float(consumo))
        )
        # Confirma los cambios en la base de datos.
        self.db.commit()

    def actualizar_detalle(self, id_detalle, id_ruta, id_modelo, consumo):
        # Actualiza un detalle existente identificado por su ID.
        # Asegura que los valores numéricos se conviertan correctamente.
        self.db.ejecutar_procedimiento(
            'actualizar_detalle',
            (int(id_detalle), int(id_ruta), int(id_modelo), float(consumo))
        )
        # Guarda los cambios realizados.
        self.db.commit()

    def eliminar_detalle(self, id_detalle):
        # Elimina un detalle según su ID usando el procedimiento almacenado correspondiente.
        self.db.ejecutar_procedimiento('sp_eliminar_detalle', (id_detalle,))
        # Aplica la operación de eliminación.
        self.db.commit()

    def listar_detalles(self):
        # Recupera todos los detalles almacenados en la base de datos.
        # fetch=True indica que se deben devolver los resultados del procedimiento.
        return self.db.ejecutar_procedimiento('mostrar_todos_detalles', (), fetch=True)
