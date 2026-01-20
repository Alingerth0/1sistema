import mysql.connector
import sys
import os

# Configuración obtenida del análisis
CONFIG = {
    'user': 'root',
    'password': '123456',
    'host': '127.0.0.1', # Forzar IPv4
    'database': 'pose',
    'raise_on_warnings': True
}

PORTS_TO_TRY = [3307, 3306, 3308]

OUTPUT_FILE = "reporte_cierres.txt"

def log_to_file(content):
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(content + "\n")

def main():
    # Limpiar archivo de salida
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
    
    log_to_file(f"--- REPORTE DE DIAGNÓSTICO DE BASE DE DATOS ---\n")
    
    conn = None
    
    # 1. Intentar conectar
    for port in PORTS_TO_TRY:
        try:
            print(f"Intentando conectar a 127.0.0.1:{port}...")
            log_to_file(f"Intentando conectar a 127.0.0.1:{port} BD: {CONFIG['database']}...")
            
            # Copiar config y añadir puerto
            current_config = CONFIG.copy()
            current_config['port'] = port
            
            conn = mysql.connector.connect(**current_config)
            
            if conn.is_connected():
                log_to_file(f"¡CONEXIÓN EXITOSA EN PUERTO {port}!\n")
                break
        except mysql.connector.Error as err:
            log_to_file(f"Fallo en puerto {port}: {err}")
            
    if not conn or not conn.is_connected():
        log_to_file("\nFATAL: No se pudo conectar a la base de datos en ningún puerto probado.")
        print("No se pudo conectar. Revise el reporte.")
        return

    try:
        cursor = conn.cursor()
        
        log_to_file("CONEXIÓN EXITOSA.\n")
        
        # 2. Listar Tablas
        print("Listando tablas...")
        cursor.execute("SHOW TABLES")
        tables = [table[0] for table in cursor.fetchall()]
        
        log_to_file(f"Total tablas encontradas: {len(tables)}")
        
        # 3. Buscar tablas de cierres
        keywords = ['z', 'x', 'close', 'report', 'fiscal']
        relevant_tables = []
        
        for table in tables:
            for kw in keywords:
                if kw in table.lower():
                    relevant_tables.append(table)
                    break # Evitar duplicados si matchea dos keywords
        
        log_to_file("\nTablas potencialmente relevantes encontradas:")
        for t in relevant_tables:
            log_to_file(f" - {t}")
            
        # 4. Inspeccionar la más probable
        # Prioridad: pos_zreport, pos_z_report, pos_fiscal_log
        target_table = None
        
        # Heurística simple para elegir la mejor tabla
        priority_list = ['pos_zreport', 'pos_z_report', 'pos_fiscal_report', 'pos_daily_report', 'pos_day_settlement']
        
        for p in priority_list:
            if p in tables:
                target_table = p
                break
        
        # Si no está en la lista prioritaria, usar la primera relevante que tenga 'z'
        if not target_table:
            for t in relevant_tables:
                if 'z' in t:
                    target_table = t
                    break
        
        if target_table:
            log_to_file(f"\n--- INSPECCIONANDO TABLA SELECCIONADA: {target_table} ---")
            
            # Obtener columnas
            cursor.execute(f"DESCRIBE {target_table}")
            columns = [col[0] for col in cursor.fetchall()]
            log_to_file(f"Columnas: {', '.join(columns)}")
            
            # Obtener datos
            # Asumimos que la primera columna es ID o fecha para ordenar
            order_col = columns[0]
            query = f"SELECT * FROM {target_table} ORDER BY {order_col} DESC LIMIT 10"
            
            log_to_file(f"\nEjecutando: {query}")
            cursor.execute(query)
            rows = cursor.fetchall()
            
            if not rows:
                log_to_file("¡La tabla está vacía!")
            else:
                log_to_file("\nÚltimos 10 registros:")
                for row in rows:
                    row_str = " | ".join([str(item) for item in row])
                    log_to_file(row_str)
                    
        else:
            log_to_file("\nNO SE PUDO IDENTIFICAR AUTOMÁTICAMENTE UNA TABLA DE CIERRES OBVIA.")
            log_to_file("Listado completo de tablas para revisión manual:")
            for t in tables:
                log_to_file(t)

        cursor.close()
        conn.close()
        print("Diagnóstico finalizado.")

    except mysql.connector.Error as err:
        error_msg = f"\nERROR DE MYSQL: {err}"
        print(error_msg)
        log_to_file(error_msg)
    except Exception as e:
        error_msg = f"\nERROR GENERAL: {e}"
        print(error_msg)
        log_to_file(error_msg)

if __name__ == "__main__":
    main()
