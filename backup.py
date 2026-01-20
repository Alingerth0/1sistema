import os
import sys
import zipfile
import datetime
import shutil

# --- Configuración ---
# Directorio raíz del proyecto (directorio actual donde se ejecuta el script)
# Se usa os.getcwd() para mayor flexibilidad, pero se puede fijar a r"D:\ESTO"
SOURCE_DIR = os.getcwd()

# Directorio de destino para los respaldos
DEST_DIR = r"C:\Users\Alt\Documents\Backups"

# Archivo de log
LOG_FILE = os.path.join(DEST_DIR, "log.txt")

# Carpetas y archivos a ignorar (nombres exactos o patrones simples)
IGNORE_LIST = [
    ".git",
    ".gemini", # Carpeta temporal de la herramienta
    "__pycache__",
    "backup.py", # No incluirse a sí mismo si está en la raíz
    "$RECYCLE.BIN",
    "System Volume Information"
]

# --- Funciones ---

def log_message(message, is_error=False):
    """
    Escribe un mensaje en la consola y en el archivo de log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}"
    
    # Imprimir en consola
    if is_error:
        print(f"ERROR: {message}", file=sys.stderr)
    else:
        print(message)
        
    # Escribir en archivo (append mode)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(formatted_message + "\n")
    except Exception as e:
        print(f"Advertencia: No se pudo escribir en el log: {e}", file=sys.stderr)

def ensure_directory_exists(path):
    """
    Verifica si un directorio existe, si no, intenta crearlo.
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
            log_message(f"Directorio creado: {path}")
        except OSError as e:
            log_message(f"Error crítico al crear directorio {path}: {e}", is_error=True)
            sys.exit(1)

def should_ignore(path, file_or_dir_name):
    """
    Determina si un archivo o directorio debe ser ignorado.
    """
    # Ignorar por nombre exacto en la lista
    if file_or_dir_name in IGNORE_LIST:
        return True
    
    # Ignorar carpetas temporales específicas (ejemplo del contexto)
    if ".gemini" in path:
        return True
        
    return False

def create_backup():
    """
    Función principal para crear el respaldo.
    """
    # 1. Preparar entorno
    ensure_directory_exists(DEST_DIR)
    
    log_message("--- Iniciando proceso de respaldo ---")
    log_message(f"Origen: {SOURCE_DIR}")
    log_message(f"Destino: {DEST_DIR}")

    # 2. Generar nombre del archivo ZIP
    timestamp_filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"backup_{timestamp_filename}.zip"
    zip_filepath = os.path.join(DEST_DIR, zip_filename)

    # 3. Crear el ZIP
    files_added = 0
    errors_encountered = 0
    
    try:
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as backup_zip:
            # Recorrer el directorio de origen
            for root, dirs, files in os.walk(SOURCE_DIR):
                
                # Filtrar directorios a ignorar 'in-place' para que os.walk no entre en ellos
                dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), d)]
                
                for file in files:
                    if should_ignore(root, file):
                        continue
                        
                    file_path = os.path.join(root, file)
                    
                    # Calcular ruta relativa para guardar dentro del zip
                    # Esto evita guardar toda la ruta absoluta C:\...
                    arcname = os.path.relpath(file_path, SOURCE_DIR)
                    
                    # Verificar si es el mismo archivo zip que estamos creando (por seguridad)
                    if os.path.abspath(file_path) == os.path.abspath(zip_filepath):
                        continue

                    try:
                        print(f"Agregando: {arcname}", end='\r') # Feedback visual en consola
                        backup_zip.write(file_path, arcname)
                        files_added += 1
                    except Exception as e:
                        log_message(f"Error al leer/agregar archivo {file_path}: {e}", is_error=True)
                        errors_encountered += 1

        print(" " * 50, end='\r') # Limpiar línea de progreso
        
        # 4. Finalización
        if errors_encountered > 0:
            log_message(f"Respaldo completado con advertencias. Archivos: {files_added}, Errores: {errors_encountered}. Archivo: {zip_filepath}")
            print(f"Respaldo completado con advertencias (ver log).")
        else:
            log_message(f"Respaldo completado con éxito. Archivos: {files_added}. Archivo: {zip_filepath}")
            print(f"Respaldo completado con éxito en {zip_filepath}")

    except Exception as e:
        log_message(f"Error CRÍTICO al crear el zip: {e}", is_error=True)
        # Intentar borrar el zip corrupto si existe
        if os.path.exists(zip_filepath):
            try:
                os.remove(zip_filepath)
                log_message("Archivo zip corrupto eliminado.")
            except:
                pass
        sys.exit(1)

if __name__ == "__main__":
    try:
        create_backup()
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError inesperado: {e}")
        sys.exit(1)
