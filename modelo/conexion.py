import mysql.connector
from mysql.connector import Error

class ConexionDB:
    _instancia = None

    def __new__(cls):
        # Implementación del patrón Singleton.
        # Garantiza que solo exista una instancia de la clase durante toda la aplicación.
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia.conexion = None
            cls._instancia.cursor = None
        return cls._instancia

    def conectar(self):
        try:
            # Si ya está conectado, no crea una nueva conexión.
            if self.conexion and self.conexion.is_connected():
                return True

            # Intenta establecer una nueva conexión.
            self.conexion = mysql.connector.connect(
                user='root',
                password='root',
                host='localhost',
                database='femaco_registro_de_rutas',
                port='3306'
            )

            # Si la conexión se estableció correctamente, crea también el cursor.
            if self.conexion.is_connected():
                self.cursor = self.conexion.cursor()
                return True

            return False

        except Error as e:
            # Se propaga el error para permitir que la capa superior lo muestre o gestione.
            raise e

    def cerrar(self):
        try:
            if self.cursor:
                self.cursor.close()
                self.cursor = None

            if self.conexion:
                self.conexion.close()
                self.conexion = None

        except Exception:
            # Se ignora cualquier error al cerrar (no crítico).
            pass

    def commit(self):
        """
        Confirma (commit) los cambios realizados en la base de datos.
        """
        if self.conexion:
            self.conexion.commit()

    def ejecutar_procedimiento(self, proc_nombre, params=(), fetch=False):
        if not self.cursor:
            raise Exception("No hay cursor: llame a conectar() antes.")

        # Ejecuta el procedimiento almacenado.
        self.cursor.callproc(proc_nombre, params)

        resultados = []

        # Obtiene todos los conjuntos de resultados generados por el procedimiento.
        for result in self.cursor.stored_results():
            resultados.extend(result.fetchall())

        # Limpia posibles result sets pendientes para evitar errores en próximas consultas.
        while self.cursor.nextset():
            pass

        # Retorna los resultados si se solicitaron.
        if fetch:
            return resultados

        return None
