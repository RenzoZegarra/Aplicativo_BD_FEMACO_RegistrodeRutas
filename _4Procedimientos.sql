-- 1. Procedimiento: agregar un vehículo validando conductor y modelo
-- Si el conductor o modelo no existe, el SP lo detecta.

DELIMITER $$

CREATE PROCEDURE sp_agregar_vehiculo(
    IN p_placa VARCHAR(10),
    IN p_id_conductor INT,
    IN p_id_modelo INT,
    IN p_marca VARCHAR(50),
    IN p_tonelaje INT,
    IN p_centro_costos VARCHAR(50)
)
BEGIN
    -- Verificar que el conductor existe
    IF (SELECT COUNT(*) FROM Conductor WHERE id_conductor = p_id_conductor) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El conductor no existe.';
    END IF;

    -- Verificar que el modelo existe
    IF (SELECT COUNT(*) FROM Modelo WHERE id_modelo = p_id_modelo) = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'El modelo no existe.';
    END IF;

    -- Insertar el vehículo
    INSERT INTO Vehiculo(placa, id_conductor, id_modelo, marca, tonelaje, centro_costos)
    VALUES (p_placa, p_id_conductor, p_id_modelo, p_marca, p_tonelaje, p_centro_costos);
END$$

DELIMITER ;


--2. Procedimiento: obtener el consumo total por ruta

--Este procedimiento suma el consumo por modelo de una ruta específica.

DELIMITER $$

CREATE PROCEDURE sp_consumo_total_por_ruta(
    IN p_id_ruta INT
)
BEGIN
    SELECT r.id_ruta,
           r.descripcion,
           SUM(d.consumo_por_modelo) AS consumo_total
    FROM Ruta r
    LEFT JOIN Detalle d ON r.id_ruta = d.id_ruta
    WHERE r.id_ruta = p_id_ruta
    GROUP BY r.id_ruta, r.descripcion;
END$$

DELIMITER ;



--3. Procedimiento con Trigger Interno: registrar historial cuando un conductor es eliminado

--Creamos:
    --Tabla de historial
    --Trigger que registra automáticamente
    --Procedimiento que elimina y activa el trigger

--3.1 Crear tabla de historial
-- Historial Conductor
CREATE TABLE IF NOT EXISTS Historial_Conductor (
    id_historial INT AUTO_INCREMENT PRIMARY KEY,
    id_conductor INT,
    nombre_conductor VARCHAR(50),
    fecha_eliminacion DATETIME
);

-- Historial ruta
CREATE TABLE IF NOT EXISTS Historial_ruta (
    id_historial_2 INT AUTO_INCREMENT PRIMARY KEY,
    id_ruta INT,
    kilometraje INT,
    tipo_ruta VARCHAR(20),
    descripcion VARCHAR(100),
    estado_ruta BOOLEAN,
    fecha_eliminacion DATETIME
);

-- Historial vehiculo
CREATE TABLE IF NOT EXISTS Historial_vehiculo (
    id_historial_3 INT AUTO_INCREMENT PRIMARY KEY,
    placa VARCHAR(10),
    id_conductor INT,
    id_modelo INT,
    marca VARCHAR(50),
    tonelaje INT,
    centro_costos VARCHAR(50),
    fecha_eliminacion DATETIME
);

-- Historial detalle
CREATE TABLE IF NOT EXISTS historial_detalle (
    id_historial_4 INT AUTO_INCREMENT PRIMARY KEY,
    id_detalle INT,
    id_ruta INT,
    id_modelo INT,
    consumo_por_modelo DECIMAL(5,2)
);

-- Historial modelo
CREATE TABLE IF NOT EXISTS historial_modelo (
    id_historial_5 INT AUTO_INCREMENT PRIMARY KEY,
    id_modelo INT,
    modelo_descripcion VARCHAR(100),
    fecha_eliminacion DATETIME
);


--3.2 Trigger BEFORE DELETE: Registra la información antes de eliminar.

--Trigger conductor eliminado
DELIMITER $$

CREATE TRIGGER tr_log_conductor_eliminado
BEFORE DELETE ON Conductor
FOR EACH ROW
BEGIN
    INSERT INTO Historial_Conductor(id_conductor, nombre_conductor, fecha_eliminacion)
    VALUES (OLD.id_conductor, OLD.nombre_conductor, NOW());
END$$

DELIMITER ;

--Trigger ruta eliminada
DELIMITER $$

CREATE TRIGGER tr_log_ruta_eliminada
BEFORE DELETE ON Ruta
FOR EACH ROW
BEGIN
    INSERT INTO Historial_ruta (
        id_ruta,
        kilometraje,
        tipo_ruta,
        descripcion,
        estado_ruta,
        fecha_eliminacion
    )
    VALUES (
        OLD.id_ruta,
        OLD.kilometraje,
        OLD.tipo_ruta,
        OLD.descripcion,
        OLD.estado_ruta,
        NOW()
    );
END$$

DELIMITER ;

--Trigger detalle eliminado
DELIMITER $$

CREATE TRIGGER tr_log_detalle_eliminado
BEFORE DELETE ON Detalle
FOR EACH ROW
BEGIN
    INSERT INTO historial_detalle (
        id_detalle,
        id_ruta,
        id_modelo,
        consumo_por_modelo
    )
    VALUES (
        OLD.id_detalle,
        OLD.id_ruta,
        OLD.id_modelo,
        OLD.consumo_por_modelo
    );
END$$

DELIMITER ;

--Trigger vehiculo eliminado
DELIMITER $$

CREATE TRIGGER tr_log_vehiculo_eliminado
BEFORE DELETE ON Vehiculo
FOR EACH ROW
BEGIN
    INSERT INTO Historial_Conductor (
        placa,
        id_conductor,
        id_modelo,
        marca,
        tonelaje,
        centro_costos,
        fecha_eliminacion
    )
    VALUES (
        OLD.placa,
        OLD.id_conductor,
        OLD.id_modelo,
        OLD.marca,
        OLD.tonelaje,
        OLD.centro_costos,
        NOW()
    );
END$$

DELIMITER ;

--Trigger modelo eliminado
DELIMITER $$

CREATE TRIGGER tr_log_modelo_eliminado
BEFORE DELETE ON Modelo
FOR EACH ROW
BEGIN
    INSERT INTO historial_modelo (
        id_modelo,
        modelo_descripcion,
        fecha_eliminacion
    )
    VALUES (
        OLD.id_modelo,
        OLD.modelo_descripcion,
        NOW()
    );
END$$

DELIMITER ;


--3.3 Procedimiento que elimina un conductor
--Este SP activa el trigger sin que el código de Python tenga que preocuparse.

--Procedimiento eliminar conductor
DELIMITER $$

CREATE PROCEDURE sp_eliminar_conductor(
    IN p_id_conductor INT
)
BEGIN
    DELETE FROM Conductor
    WHERE id_conductor = p_id_conductor;
END$$

DELIMITER ;

--Procedimiento eliminar ruta
DELIMITER $$

CREATE PROCEDURE sp_eliminar_ruta(
    IN p_id_ruta INT
)
BEGIN
    DELETE FROM Ruta
    WHERE id_ruta = p_id_ruta;
END$$

DELIMITER ;

--Procedimiento eliminar detalle
DELIMITER $$

CREATE PROCEDURE sp_eliminar_detalle(
    IN p_id_detalle INT
)
BEGIN
    DELETE FROM Detalle
    WHERE id_detalle = p_id_detalle;
END$$

DELIMITER ;

--Procedimiento eliminar vehiculo
DELIMITER $$

CREATE PROCEDURE sp_eliminar_vehiculo(
    IN p_placa VARCHAR(10)
)
BEGIN
    DELETE FROM Vehiculo
    WHERE placa = p_placa;
END$$

DELIMITER ;

--Procedimiento eliminar modelo
DELIMITER $$

CREATE PROCEDURE sp_eliminar_modelo(
    IN p_id_modelo INT
)
BEGIN
    DELETE FROM Modelo
    WHERE id_modelo = p_id_modelo;
END$$

DELIMITER ;
