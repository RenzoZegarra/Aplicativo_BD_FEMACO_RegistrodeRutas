-- Consultas de SQL

-- Consulta 1: Vehículos que tienen conductor asignado.
SELECT 
    v.placa,
    v.marca,
    v.tonelaje,
    c.nombre_conductor
FROM Vehiculo v
INNER JOIN Conductor c ON v.id_conductor = c.id_conductor;

-- Consulta 2: Rutas que están activas actualmente.
SELECT 
    id_ruta,
    descripcion,
    tipo_ruta,
    kilometraje
FROM Ruta
WHERE estado_ruta = 1;

-- Consulta 3: Descripción de las rutas y cuántos detalles tiene cada una.
SELECT 
    r.descripcion,
    COUNT(d.id_detalle) AS cantidad_detalles
FROM Ruta r
LEFT JOIN Detalle d ON r.id_ruta = d.id_ruta
GROUP BY r.id_ruta, r.descripcion;

-- Consulta 4: Las 3 rutas con mejor rendimiento.
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

-- Consulta 5: Mostrar los vehículos con su modelo y centro de costos.
SELECT 
    v.placa,
    v.marca,
    m.modelo_descripcion,
    v.centro_costos
FROM Vehiculo v
INNER JOIN Modelo m ON v.id_modelo = m.id_modelo;

-- Consulta 6: Mostrar los modelos más usados por vehículos.
SELECT 
    m.modelo_descripcion,
    COUNT(v.placa) AS cantidad_vehiculos
FROM Modelo m
LEFT JOIN Vehiculo v ON m.id_modelo = v.id_modelo
GROUP BY m.id_modelo, m.modelo_descripcion
ORDER BY cantidad_vehiculos DESC;

-- Consulta 7: Mostrar el consumo promedio por modelo en todas las rutas.
SELECT 
    m.modelo_descripcion,
    ROUND(AVG(d.consumo_por_modelo), 2) AS consumo_promedio
FROM Modelo m
INNER JOIN Detalle d ON m.id_modelo = d.id_modelo
GROUP BY m.id_modelo, m.modelo_descripcion
ORDER BY consumo_promedio ASC;

-- Consulta 8: Mostrar los vehículos con tonelaje superior a 8 toneladas
SELECT 
    placa,
    marca,
    tonelaje,
    centro_costos
FROM Vehiculo
WHERE tonelaje > 8;

-- Consulta 9: Mostrar las rutas por tipo (Local o Provincial) con cantidad total.
SELECT 
    tipo_ruta,
    COUNT(*) AS cantidad_rutas
FROM Ruta
GROUP BY tipo_ruta;


-- Consulta 10: Mostrar las rutas inactivas
SELECT 
    id_ruta,
    descripcion,
    tipo_ruta,
    kilometraje
FROM Ruta
WHERE estado_ruta = 0;

-- CONSULTAS QUE USAN LOS INDICES

-- Consulta 11: Consultar los vehículos agrupados por modelo
-- Usa el índice: idx_id_modelo_vehiculo (Vehiculo.id_modelo)
SELECT v.id_modelo, COUNT(*) AS cantidad
FROM Vehiculo v
GROUP BY v.id_modelo;

-- Consulta 12: Buscar un modelo específico
-- Usa el índice: idx_id_modelo (Modelo.id_modelo)
SELECT * FROM Modelo
WHERE id_modelo = 10;