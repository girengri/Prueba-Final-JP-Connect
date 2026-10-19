# 📊 Prueba Final Semillero DATA - JP Connect

![Python](https://img.shields.io/badge/Python-3.9-blue?logo=python&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-F2C811?logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-2.0.3-150458?logo=pandas&logoColor=white)
![ChatGPT](https://img.shields.io/badge/ChatGPT-00A67E?logo=openai&logoColor=white)

**Autor:** Giovany Rendon Grisales 
**Fecha:** Octubre 2026

---

## 📌 1. Contexto del Problema
JP Connect experimentó una caída en la retención de sus usuarios activos en el último trimestre. El objetivo de este proyecto fue identificar las causas raíz, limpiar la base de datos, analizar los motivos de deserción y proponer un plan de acción automatizado al Director de Operaciones.

## 🏗️ 2. Arquitectura de Datos y Proceso ETL
Para garantizar la calidad de los datos, se diseñó un pipeline ETL completo:
1. **Extracción y Transformación (Python):** Se usó `Pandas` para limpiar el Excel original. El script realiza las siguientes acciones:
   - Estandarización de textos (mayúsculas/minúsculas y eliminación de espacios).
   - Eliminación de registros duplicados mediante `drop_duplicates()`.
   - Corrección de formatos de fecha mixtos con `to_datetime()`.
   - **Manejo de Nulos:** Se imputó la mediana en la columna de satisfacción del cliente para evitar sesgos estadísticos.
2. **Carga (MySQL):** Los datos limpios se cargaron en una base de datos relacional. Se crearon llaves primarias y foráneas para garantizar la integridad.
3. **Modelado (Power BI):** Se implementó un **Modelo Estrella**. La tabla `clientes_tlp` actúa como dimensión central y se conecta en relación 1:N con las tablas de hechos `tickets_soporte` y `uso_servicios`.

## 🛠️ 3. Tecnologías Utilizadas
*   **Python (Pandas, MySQL Connector):** Automatización del ETL.
*   **MySQL:** Almacenamiento estructurado y consultas analíticas.
*   **Power BI:** Visualización de datos y Storytelling.
*   **ChatGPT (IA):** Asistencia en generación de código (Text-to-SQL).

## 📈 4. Hallazgos y Consultas SQL Clave
*   *Clientes Activos:* Se segmentaron los clientes por tipo de suscripción (Básico, Premium, Enterprise).
*   *Tiempos de Resolución:* Se identificó que la categoría **[Falla Técnica]** tiene el mayor tiempo de resolución promedio.
*   *Análisis con IA:* Mediante un prompt en ChatGPT, se generó la consulta SQL para identificar el Top 5 de clientes con mayor consumo de GB, permitiendo priorizar su atención.

## 💡 5. Recomendación de Negocio (Storytelling)
Basado en el dashboard interactivo:
> *"La tasa de deserción global es del **20%**. El gráfico evidencia que la mayor carga operativa se debe a **Falla Técnica**. Se recomienda implementar alertas automáticas cuando un ticket de esta categoría supere las 8 horas de resolución, y priorizar a los Top 5 clientes con mayor consumo de API para mitigar la deserción y proteger los ingresos."*

---

## 🚀 6. Guía de Instalación y Ejecución (Para el Evaluador)

Dado que este es un proyecto de análisis local, sigue estos pasos para replicar el entorno y visualizar el modelo en Power BI:

### Paso 1: Configurar la Base de Datos (MySQL)
1. Abre **MySQL Workbench** y crea la base de datos ejecutando:
   ```sql
   CREATE DATABASE IF NOT EXISTS jp_connect_db;
2. Abre el archivo `1_ETL/etl_jp_connect.py` en tu editor de código (PyCharm, VS Code, etc.).
3. ⚠️ **IMPORTANTE:** En la línea 12 del script, cambia `'TU_CONTRASEÑA_AQUI'` por la contraseña de tu usuario `root` de MySQL local.
4. Ejecuta el script de Python. Esto creará automáticamente las 3 tablas y cargará los datos limpios.

### Paso 2: Configurar Power BI
1. Abre el archivo `3_PowerBI/Dashboard_JP_Connect.pbix`.
2. Si Power BI te pide credenciales o da error de conexión, ve a la cinta superior: **Inicio > Transformar datos > Configuración del origen de datos**.
3. Selecciona la conexión a MySQL y haz clic en **"Cambiar origen"** o **"Editar permisos"** e ingresa la contraseña de tu MySQL local.
4. Haz clic en **"Actualizar"** para que los gráficos carguen los datos.

### Paso 3: ¿Cómo ver el Modelo Estrella?
Si solo deseas verificar el diseño relacional sin ejecutar los datos:
1. Abre el archivo `.pbix` en Power BI.
2. En el menú lateral izquierdo, haz clic en el **tercer icono (Vista de Modelo)**.
3. Allí podrás ver gráficamente cómo la tabla `clientes_tlp` se conecta con llaves foráneas a `tickets_soporte` y `uso_servicios`.

Proyecto desarrollado para la prueba final del Semillero DATA.