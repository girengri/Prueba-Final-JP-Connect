-- NUMERO DE CLIENTES ACTIVOS POR TIPO DE SUSCRIPCION
SELECT 
    tipo_suscripcion,
    COUNT(id_cliente) AS total_clientes_activos
FROM
    clientes_tlp
WHERE
    estado = 'Activo'
GROUP BY tipo_suscripcion
ORDER BY total_clientes_activos DESC;

-- TIEMPO PROMEDIO DE RESPUESTAS DE LOS TICKES POR CATEGORIA
SELECT
categoria,
ROUND(AVG(tiempo_resolucion_horas), 2) AS promedio_horas_respuesta
FROM
tickets_soporte
GROUP BY categoria
ORDER BY promedio_horas_respuesta DESC;

