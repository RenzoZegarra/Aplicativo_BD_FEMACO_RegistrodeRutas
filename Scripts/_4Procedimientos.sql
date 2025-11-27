--1. Procedimientos de INSERCION
--Modelo
DELIMITER $$

CREATE PROCEDURE insertar_modelo(
    IN p_modelo_descripcion VARCHAR(100)
)
BEGIN
    INSERT INTO Modelo(modelo_descripcion)
    VALUES (p_modelo_descripcion);
END$$

DELIMITER ;

--Conductor
DELIMITER $$

CREATE PROCEDURE insertar_conductor(
    IN p_nombre_conductor VARCHAR(50)
)
BEGIN
    INSERT INTO Conductor(nombre_conductor)
    VALUES (p_nombre_conductor);
END$$

DELIMITER ;

--Ruta
DELIMITER $$

CREATE PROCEDURE insertar_ruta(
    IN p_kilometraje INT,
    IN p_tipo_ruta VARCHAR(20),
    IN p_descripcion VARCHAR(100),
    IN p_estado_ruta INT
)
BEGIN
    -- Ajustar kilometraje si es negativo
    IF p_kilometraje < 0 THEN
        SET p_kilometraje = 0;
    END IF;

    -- Ajustar estado de ruta a 0 o 1
    IF p_estado_ruta < 0 THEN
        SET p_estado_ruta = 0;
    ELSEIF p_estado_ruta > 1 THEN
        SET p_estado_ruta = 1;
    END IF;

    -- Ajustar tipo de ruta si es inválido
    IF p_tipo_ruta NOT IN ('Local','Provincial') THEN
        SET p_tipo_ruta = 'Sin tipo de ruta';
    END IF;

    INSERT INTO Ruta(kilometraje, tipo_ruta, descripcion, estado_ruta)
    VALUES (p_kilometraje, p_tipo_ruta, p_descripcion, p_estado_ruta);
END$$

DELIMITER ;


--Vehiculo
DELIMITER $$

CREATE PROCEDURE insertar_vehiculo(
    IN p_placa VARCHAR(10),
    IN p_id_conductor INT,
    IN p_id_modelo INT,
    IN p_marca VARCHAR(50),
    IN p_tonelaje INT,
    IN p_centro_costos VARCHAR(50)
)
BEGIN
    -- Ajustar tonelaje si es negativo
    IF p_tonelaje < 0 THEN
        SET p_tonelaje = 0;
    END IF;

    INSERT INTO Vehiculo(placa, id_conductor, id_modelo, marca, tonelaje, centro_costos)
    VALUES (p_placa, p_id_conductor, p_id_modelo, p_marca, p_tonelaje, p_centro_costos);
END$$

DELIMITER ;


--Detalle
DELIMITER $$

CREATE PROCEDURE insertar_detalle(
    IN p_id_ruta INT,
    IN p_id_modelo INT,
    IN p_consumo_por_modelo DECIMAL(5,2)
)
BEGIN
    -- Ajustar consumo si es negativo
    IF p_consumo_por_modelo < 0 THEN
        SET p_consumo_por_modelo = 0;
    END IF;

    INSERT INTO Detalle(id_ruta, id_modelo, consumo_por_modelo)
    VALUES (p_id_ruta, p_id_modelo, p_consumo_por_modelo);
END$$

DELIMITER ;

--2. PROCEDIMIENTOS DE CONSULTA

DELIMITER $$

CREATE PROCEDURE consulta1_vehiculos_con_conductor()
BEGIN
    SELECT 
        v.placa,
        v.marca,
        v.tonelaje,
        c.nombre_conductor
    FROM Vehiculo v
    INNER JOIN Conductor c ON v.id_conductor = c.id_conductor;
END$$

CREATE PROCEDURE consulta2_rutas_activas()
BEGIN
    SELECT 
        id_ruta,
        descripcion,
        tipo_ruta,
        kilometraje
    FROM Ruta
    WHERE estado_ruta = 1;
END$$

CREATE PROCEDURE consulta3_rutas_detalles()
BEGIN
    SELECT 
        r.descripcion,
        COUNT(d.id_detalle) AS cantidad_detalles
    FROM Ruta r
    LEFT JOIN Detalle d ON r.id_ruta = d.id_ruta
    GROUP BY r.id_ruta, r.descripcion;
END$$

CREATE PROCEDURE consulta4_top_rendimiento()
BEGIN
    SELECT 
        r.descripcion,
        r.kilometraje,
        ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio,
        ROUND(r.kilometraje / AVG(d.consumo_por_modelo), 2) AS rendimiento
    FROM Ruta r
    INNER JOIN Detalle d ON r.id_ruta = d.id_ruta
    GROUP BY r.id_ruta, r.descripcion, r.kilometraje
    ORDER BY rendimiento DESC
    LIMIT 3;
END$$

CREATE PROCEDURE consulta5_vehiculos_modelo()
BEGIN
    SELECT 
        v.placa,
        v.marca,
        m.modelo_descripcion,
        v.centro_costos
    FROM Vehiculo v
    INNER JOIN Modelo m ON v.id_modelo = m.id_modelo;
END$$

CREATE PROCEDURE consulta6_modelos_usados()
BEGIN
    SELECT 
        m.modelo_descripcion,
        COUNT(v.placa) AS cantidad_vehiculos
    FROM Modelo m
    LEFT JOIN Vehiculo v ON m.id_modelo = v.id_modelo
    GROUP BY m.id_modelo, m.modelo_descripcion
    ORDER BY cantidad_vehiculos DESC;
END$$

CREATE PROCEDURE consulta7_consumo_promedio_modelo()
BEGIN
    SELECT 
        m.modelo_descripcion,
        ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio
    FROM Modelo m
    INNER JOIN Detalle d ON m.id_modelo = d.id_modelo
    GROUP BY m.id_modelo, m.modelo_descripcion
    ORDER BY consumo_promedio ASC;
END$$

CREATE PROCEDURE consulta8_vehiculos_tonelaje()
BEGIN
    SELECT 
        placa,
        marca,
        tonelaje,
        centro_costos
    FROM Vehiculo
    WHERE tonelaje > 8;
END$$

CREATE PROCEDURE consulta9_rutas_tipo()
BEGIN
    SELECT 
        tipo_ruta,
        COUNT(*) AS cantidad_rutas
    FROM Ruta
    GROUP BY tipo_ruta;
END$$

CREATE PROCEDURE consulta10_rutas_inactivas()
BEGIN
    SELECT 
        id_ruta,
        descripcion,
        tipo_ruta,
        kilometraje
    FROM Ruta
    WHERE estado_ruta = 0;
END$$

CREATE PROCEDURE consulta11_vehiculos_por_modelo()
BEGIN
    SELECT v.id_modelo, COUNT(*) AS cantidad
    FROM Vehiculo v
    GROUP BY v.id_modelo;
END$$

CREATE PROCEDURE consulta12_buscar_modelo(IN p_id_modelo INT)
BEGIN
    SELECT * FROM Modelo
    WHERE id_modelo = p_id_modelo;
END$$

DELIMITER ;

--PROCEDIMIENTOS DE LISTADO

DELIMITER $$

CREATE PROCEDURE mostrar_todas_rutas()
BEGIN
    SELECT * FROM Ruta;
END$$

CREATE PROCEDURE mostrar_todos_vehiculos()
BEGIN
    SELECT * FROM Vehiculo;
END$$

CREATE PROCEDURE mostrar_todos_conductores()
BEGIN
    SELECT * FROM Conductor;
END$$

CREATE PROCEDURE mostrar_todos_modelos()
BEGIN
    SELECT * FROM Modelo;
END$$

CREATE PROCEDURE mostrar_todos_detalles()
BEGIN
    SELECT * FROM Detalle;
END$$

DELIMITER ;

--3. Procedimientos de ACTUALIZACION
--Modelo
DELIMITER $$

CREATE PROCEDURE actualizar_modelo(
    IN p_id_modelo INT,
    IN p_modelo_descripcion VARCHAR(100)
)
BEGIN
    UPDATE Modelo
    SET modelo_descripcion = p_modelo_descripcion
    WHERE id_modelo = p_id_modelo;
END$$

DELIMITER ;


--Conductor
DELIMITER $$

CREATE PROCEDURE actualizar_conductor(
    IN p_id_conductor INT,
    IN p_nombre_conductor VARCHAR(50)
)
BEGIN
    UPDATE Conductor
    SET nombre_conductor = p_nombre_conductor
    WHERE id_conductor = p_id_conductor;
END$$

DELIMITER ;


--Ruta
DELIMITER $$

CREATE PROCEDURE actualizar_ruta(
    IN p_id_ruta INT,
    IN p_kilometraje INT,
    IN p_tipo_ruta VARCHAR(20),
    IN p_descripcion VARCHAR(100),
    IN p_estado_ruta INT
)
BEGIN
    -- Ajustar kilometraje si es negativo
    IF p_kilometraje < 0 THEN
        SET p_kilometraje = 0;
    END IF;

    -- Ajustar estado de ruta a 0 o 1
    IF p_estado_ruta < 0 THEN
        SET p_estado_ruta = 0;
    ELSEIF p_estado_ruta > 1 THEN
        SET p_estado_ruta = 1;
    END IF;

    -- Ajustar tipo de ruta si es inválido
    IF p_tipo_ruta NOT IN ('Local','Provincial') THEN
        SET p_tipo_ruta = 'Sin tipo de ruta';
    END IF;

    UPDATE Ruta
    SET kilometraje = p_kilometraje,
        tipo_ruta = p_tipo_ruta,
        descripcion = p_descripcion,
        estado_ruta = p_estado_ruta
    WHERE id_ruta = p_id_ruta;
END$$

DELIMITER ;


--Vehiculo
DELIMITER $$

CREATE PROCEDURE actualizar_vehiculo(
    IN p_placa VARCHAR(10),
    IN p_id_conductor INT,
    IN p_id_modelo INT,
    IN p_marca VARCHAR(50),
    IN p_tonelaje INT,
    IN p_centro_costos VARCHAR(50)
)
BEGIN
    -- Ajustar tonelaje si es negativo
    IF p_tonelaje < 0 THEN
        SET p_tonelaje = 0;
    END IF;

    UPDATE Vehiculo
    SET id_conductor = p_id_conductor,
        id_modelo = p_id_modelo,
        marca = p_marca,
        tonelaje = p_tonelaje,
        centro_costos = p_centro_costos
    WHERE placa = p_placa;
END$$

DELIMITER ;


--Detalle
DELIMITER $$

CREATE PROCEDURE actualizar_detalle(
    IN p_id_detalle INT,
    IN p_id_ruta INT,
    IN p_id_modelo INT,
    IN p_consumo_por_modelo DECIMAL(5,2)
)
BEGIN
    -- Ajustar consumo si es negativo
    IF p_consumo_por_modelo < 0 THEN
        SET p_consumo_por_modelo = 0;
    END IF;

    UPDATE Detalle
    SET id_ruta = p_id_ruta,
        id_modelo = p_id_modelo,
        consumo_por_modelo = p_consumo_por_modelo
    WHERE id_detalle = p_id_detalle;
END$$

DELIMITER ;




--4. Procedimiento con Trigger Interno: registrar historial

--Creamos:
    --Tabla de historial
    --Trigger que registra automáticamente
    --Procedimiento que elimina y activa el trigger

--4.1 Crear tabla de historial
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


--4.2 Trigger BEFORE DELETE: Registra la información antes de eliminar.

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
    INSERT INTO Historial_vehiculo (
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


--4.3 Procedimiento que elimina un conductor
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


DELIMITER $$

CREATE PROCEDURE buscar_conductor(IN nombre_buscar VARCHAR(100))
BEGIN
    SELECT COUNT(*) AS total
    FROM conductor
    WHERE nombre_conductor = nombre_buscar;
END $$

DELIMITER ;


