import pandas as pd
import mysql.connector
from mysql.connector import Error
import numpy as np

# ==========================================
# 1. CONFIGURACIÓN
# ==========================================
# Usamos la 'r' al inicio para que Python lea la ruta de Windows sin errores. PON ACA LA RUTA DEL ARCHIVO EXCEL
ruta_excel = r''
# ⚠️ CAMBIA ESTO POR TU CONTRASEÑA REAL DE MYSQL
password_mysql = ''

try:
    print("📂 Cargando las 3 hojas del Excel...")
    # Leemos cada hoja del mismo archivo
    df_clientes = pd.read_excel(ruta_excel, sheet_name='clientes_tlp')
    df_uso = pd.read_excel(ruta_excel, sheet_name='uso_servicios')
    df_tickets = pd.read_excel(ruta_excel, sheet_name='tickets_soporte')

    # ==========================================
    # 2. LIMPIEZA DE DATOS (TRANSFORMACIÓN)
    # ==========================================
    print("🧹 Limpiando hoja de Clientes...")
    for col in ['nombre_empresa', 'tipo_suscripcion', 'estado']:
        df_clientes[col] = df_clientes[col].astype(str).str.strip()

    df_clientes['tipo_suscripcion'] = df_clientes['tipo_suscripcion'].str.capitalize().replace('Basico', 'Básico')
    df_clientes['estado'] = df_clientes['estado'].str.capitalize()

    # Eliminar duplicados y arreglar fechas mixtas
    df_clientes = df_clientes.drop_duplicates(subset=['id_cliente'], keep='first')
    df_clientes['fecha_registro'] = pd.to_datetime(df_clientes['fecha_registro'], format='mixed', dayfirst=True,
                                                   errors='coerce')
    df_clientes['fecha_registro'] = df_clientes['fecha_registro'].dt.strftime('%Y-%m-%d')

    print("🧹 Limpiando hoja de Uso de Servicios...")
    # Corregir comas por puntos en los GB
    df_uso['gigabytes_consumidos'] = df_uso['gigabytes_consumidos'].astype(str).str.replace(',', '.')
    df_uso['gigabytes_consumidos'] = pd.to_numeric(df_uso['gigabytes_consumidos'], errors='coerce')

    print("🧹 Limpiando hoja de Tickets de Soporte...")
    # Corregir comas por puntos en el tiempo de resolución
    df_tickets['tiempo_resolucion_horas'] = df_tickets['tiempo_resolucion_horas'].astype(str).str.replace(',', '.')
    df_tickets['tiempo_resolucion_horas'] = pd.to_numeric(df_tickets['tiempo_resolucion_horas'], errors='coerce')

    # Estrategia de Nulos para Satisfacción: Rellenar con la mediana
    mediana_satisfaccion = df_tickets['satisfaccion_cliente'].median()
    df_tickets['satisfaccion_cliente'] = df_tickets['satisfaccion_cliente'].fillna(mediana_satisfaccion)
    df_tickets['satisfaccion_cliente'] = df_tickets['satisfaccion_cliente'].astype(int)

    # Limpiar NaNs generales para que MySQL los acepte como NULL
    df_clientes = df_clientes.replace({np.nan: None})
    df_uso = df_uso.replace({np.nan: None})
    df_tickets = df_tickets.replace({np.nan: None})

    # ==========================================
    # 3. CONEXIÓN Y CREACIÓN DE TABLAS EN MYSQL
    # ==========================================
    print("🔌 Conectando a MySQL...")
    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password=password_mysql,
        database='jp_connect_db'
    )
    cursor = conexion.cursor()

    # Eliminar tablas en orden inverso por las llaves foráneas (por si ejecutas el script varias veces)
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
    cursor.execute("DROP TABLE IF EXISTS tickets_soporte;")
    cursor.execute("DROP TABLE IF EXISTS uso_servicios;")
    cursor.execute("DROP TABLE IF EXISTS clientes_tlp;")
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    print("🛠️ Creando tablas con Llaves Primarias y Foráneas...")

    # 1. Tabla Clientes
    cursor.execute("""
    CREATE TABLE clientes_tlp (
        id_cliente INT PRIMARY KEY,
        nombre_empresa VARCHAR(150),
        fecha_registro DATE,
        tipo_suscripcion VARCHAR(50),
        estado VARCHAR(20)
    );
    """)

    # 2. Tabla Uso de Servicios
    cursor.execute("""
    CREATE TABLE uso_servicios (
        id_registro INT PRIMARY KEY,
        id_cliente INT,
        mes_evaluado VARCHAR(10),
        consultas_api INT,
        gigabytes_consumidos FLOAT,
        FOREIGN KEY (id_cliente) REFERENCES clientes_tlp(id_cliente)
    );
    """)

    # 3. Tabla Tickets de Soporte
    cursor.execute("""
    CREATE TABLE tickets_soporte (
        id_ticket INT PRIMARY KEY,
        id_cliente INT,
        categoria VARCHAR(50),
        tiempo_resolucion_horas FLOAT,
        satisfaccion_cliente INT,
        FOREIGN KEY (id_cliente) REFERENCES clientes_tlp(id_cliente)
    );
    """)

    # ==========================================
    # 4. CARGA DE DATOS (LOAD)
    # ==========================================
    print("📥 Insertando datos en MySQL...")

    sql_clientes = "INSERT INTO clientes_tlp VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql_clientes, df_clientes.values.tolist())

    sql_uso = "INSERT INTO uso_servicios VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql_uso, df_uso.values.tolist())

    sql_tickets = "INSERT INTO tickets_soporte VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(sql_tickets, df_tickets.values.tolist())

    conexion.commit()
    print(f"🚀 ¡Éxito! Base de datos creada y poblada correctamente.")
    print(f"Registros -> Clientes: {len(df_clientes)} | Uso: {len(df_uso)} | Tickets: {len(df_tickets)}")

except Error as e:
    print(f"❌ Error en MySQL: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")
finally:
    if 'conexion' in locals() and conexion.is_connected():
        cursor.close()
        conexion.close()
        print("🔒 Conexión cerrada.")