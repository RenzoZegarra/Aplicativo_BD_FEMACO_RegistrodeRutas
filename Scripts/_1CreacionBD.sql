-- Creación de la base de datos
CREATE DATABASE IF NOT EXISTS femaco_registro_de_rutas;
USE femaco_registro_de_rutas;

-- Eliminación de tablas en caso existan
DROP TABLE IF EXISTS Detalle;
DROP TABLE IF EXISTS Vehiculo;
DROP TABLE IF EXISTS Ruta;
DROP TABLE IF EXISTS Modelo;
DROP TABLE IF EXISTS Conductor;

-- Creación de tablas

CREATE TABLE Conductor (
    id_conductor INT PRIMARY KEY AUTO_INCREMENT,
    nombre_conductor VARCHAR(50)
);

CREATE TABLE Modelo (
    id_modelo INT PRIMARY KEY AUTO_INCREMENT,
    modelo_descripcion VARCHAR(100)
);

CREATE TABLE Ruta (
    id_ruta INT PRIMARY KEY AUTO_INCREMENT,
    kilometraje INT,
    tipo_ruta VARCHAR(20),
    descripcion VARCHAR(100),
    estado_ruta BOOLEAN
);

CREATE TABLE Vehiculo (
    placa VARCHAR(10) PRIMARY KEY,
    id_conductor INT,
    id_modelo INT,
    marca VARCHAR(50),
    tonelaje INT,
    centro_costos VARCHAR(50),
    FOREIGN KEY (id_conductor) REFERENCES Conductor(id_conductor),
    FOREIGN KEY (id_modelo) REFERENCES Modelo(id_modelo)
);

CREATE TABLE Detalle (
    id_detalle INT PRIMARY KEY AUTO_INCREMENT,
    id_ruta INT,
    id_modelo INT,
    consumo_por_modelo DECIMAL(5,2),
    FOREIGN KEY (id_ruta) REFERENCES Ruta(id_ruta),
    FOREIGN KEY (id_modelo) REFERENCES Modelo(id_modelo)
);

-- Creacion de indices de la tabla RUTA
-- Índice primario
CREATE UNIQUE INDEX idx_id_ruta
ON Ruta(id_ruta);

-- Índice secundario en estado_ruta
CREATE INDEX idx_estado_ruta
ON Ruta(estado_ruta);



-- Creación de indices de la tabla DETALLE

-- Índice primario
CREATE UNIQUE INDEX idx_id_detalle
ON Detalle(id_detalle);

-- Índice foráneo hacia Ruta
CREATE INDEX idx_id_ruta
ON Detalle(id_ruta);

-- Índice foráneo hacia Modelo
CREATE INDEX idx_id_modelo
ON Detalle(id_modelo);



-- Creación de indices de la tabla MODELO

-- Índice primario (PRIMARY KEY)
CREATE UNIQUE INDEX idx_id_modelo
ON Modelo(id_modelo);


-- Creación de indices de la tabla VEHICULO

-- Índice primario
CREATE UNIQUE INDEX idx_placa
ON Vehiculo(placa);

-- Índice foráneo hacia Conductor
CREATE INDEX idx_id_conductor
ON Vehiculo(id_conductor);

-- Índice foráneo hacia Modelo
CREATE INDEX idx_id_modelo
ON Vehiculo(id_modelo);

-- Creación de indices de la tabla CONDUCTOR

-- Índice primario
CREATE UNIQUE INDEX idx_id_conductor
ON Conductor(id_conductor);



-- COMANDO: SOURCE C:/Users/LENOVO/1_Zegarra/_1CreacionBD.sql;