import time
import requests
import subprocess
import os
import threading
import sys
import json
import tkinter as tk
from tkinter import messagebox

# --- COMPROBACION DE DEPENDENCIAS ---
try:
    import win32print
    import win32timezone
    from flask import Flask, request, jsonify
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
except ImportError as e:
    print(f"ERROR: Falta la libreria {e}. Instale requirements.txt")
    sys.exit(1)

# --- CONFIGURACION MAESTRA ---
URL_LICENCIAS = "https://alingerth0.github.io/1sistema/licencias.json"
PRINTER_NAME = "IMP1"
PORT_HTTP = 8876

# Directorios
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, "..", "..")) 
SERVICE_BAT = os.path.join(PROJECT_ROOT, "1SS", "1.bat")
ATV_FILE = os.path.join(BASE_DIR, "data", "config", "atv.txt")
RIF_FILE = os.path.join(BASE_DIR, "rif.txt")
LOG_DIR = os.path.join(BASE_DIR, "temp", "pos_assistant_logs")

os.makedirs(LOG_DIR, exist_ok=True)

app = Flask(__name__)

# --- LOGICA DE IMPRESION Y PARSING ---

def parse_and_send_to_printer(content_str):
    """
    Traduce el formato PHP (>27,64) a bytes reales y envia a la impresora IMP1.
    """
    raw_data = bytearray()
    lines = content_str.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line in ["[[IMP1", "]]", "receipt_printer"]:
            continue
            
        if line.startswith(">"):
            # Es un comando de control (ej: >27,112,0,25,250 para abrir gaveta)
            parts = line.replace(">", "").split(",")
            for p in parts:
                try:
                    val = int(p, 16) if "x" in p else int(p)
                    raw_data.append(val)
                except:
                    pass
        else:
            # Texto normal
            raw_data.extend(line.encode("cp850", errors="replace"))
            raw_data.append(10) # Line Feed

    if raw_data:
        try:
            hPrinter = win32print.OpenPrinter(PRINTER_NAME)
            hJob = win32print.StartDocPrinter(hPrinter, 1, ("POS Ticket", None, "RAW"))
            win32print.StartPagePrinter(hPrinter)
            win32print.WritePrinter(hPrinter, raw_data)
            win32print.EndPagePrinter(hPrinter)
            win32print.EndDocPrinter(hPrinter)
            win32print.ClosePrinter(hPrinter)
            return True
        except Exception as e:
            print(f"Error fisico en impresora: {e}")
    return False

# --- SERVIDOR HTTP (PUERTO 8876) ---

@app.route('/print', methods=['POST'])
def http_print():
    data = request.json or request.form
    content = data.get('data', '')
    print("Recibida peticion de impresion via HTTP")
    if parse_and_send_to_printer(content):
        return jsonify({"status": 1, "msg": "Impreso"})
    return jsonify({"status": 0, "msg": "Error de impresora"}), 500

@app.route('/scale', methods=['POST'])
def http_scale():
    # Simula una balanza retornando 0.000 si no hay hardware conectado
    return jsonify({"status": 1, "data": "0.000"})

@app.route('/dzc', methods=['POST'])
def http_dzc():
    # Visor de cliente (opcional)
    return jsonify({"status": 1})

# --- MONITOR DE CARPETA (FILESYSTEM) ---

class LegacyPrintHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):
            time.sleep(0.3) # Esperar a que el archivo se libere
            try:
                with open(event.src_path, "r", encoding="latin-1", errors="ignore") as f:
                    content = f.read()
                if "[[IMP1" in content or "receipt_printer" in content:
                    parse_and_send_to_printer(content)
                    # Opcional: Limpiar el archivo para evitar duplicados
                    # open(event.src_path, 'w').close()
            except:
                pass

# --- GESTION DE LICENCIA ---

def get_hwid():
    try:
        return subprocess.check_output('wmic csproduct get uuid').decode().split('\n')[1].strip()
    except:
        return "HWID-GENERIC-POS"

def check_license_online(rif_manual=None, code_manual=None):
    hwid = get_hwid()
    rif = rif_manual or ""
    
    if not rif and os.path.exists(RIF_FILE):
        with open(RIF_FILE, "r") as f: rif = f.read().strip()
    
    if not rif: return False, "Falta RIF"

    try:
        r = requests.get(URL_LICENCIAS, timeout=8)
        if r.status_code != 200: return False, "Servidor de licencias offline"
        
        data = r.json()
        for c in data.get("clientes", []):
            if c["rif"].upper() == rif.upper():
                # Si es activacion inicial, validar codigo
                if code_manual and c.get("codigo_activacion") != code_manual:
                    return False, "Código de activación incorrecto"
                
                # Validar PC (HWID)
                if c["hwid"] != "ANY" and c["hwid"] != hwid:
                    return False, "Esta licencia pertenece a otra computadora"
                
                # Validar Status y Fecha
                if c["status"] == "activo":
                    fecha_exp = time.strptime(c["expiracion"], "%Y-%m-%d")
                    if time.mktime(fecha_exp) > time.time():
                        return True, c["nombre"]
                    return False, "Licencia expirada"
        return False, "RIF no registrado"
    except Exception as e:
        return False, f"Error de red: {e}"

# --- INTERFAZ DE ACTIVACION ---

def show_activation_ui():
    root = tk.Tk()
    root.title("Activación POS Assistant")
    root.geometry("350x280")
    root.attributes("-topmost", True)
    
    tk.Label(root, text="SISTEMA NO ACTIVADO", fg="red", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(root, text="RIF del Cliente:").pack()
    ent_rif = tk.Entry(root, width=30)
    ent_rif.pack()
    
    tk.Label(root, text="Código de Activación:").pack(pady=5)
    ent_code = tk.Entry(root, width=30, show="*")
    ent_code.pack()

    def do_act():
        rif = ent_rif.get().strip()
        code = ent_code.get().strip()
        ok, msg = check_license_online(rif, code)
        if ok:
            with open(RIF_FILE, "w") as f: f.write(rif)
            messagebox.showinfo("Exito", f"Activado para: {msg}")
            root.destroy()
        else:
            messagebox.showerror("Error", msg)

    tk.Button(root, text="ACTIVAR AHORA", command=do_act, bg="green", fg="white", width=20).pack(pady=20)
    root.mainloop()

# --- MAIN ---

if __name__ == "__main__":
    print("Iniciando POS Assistant...")
    
    # 1. Validar Licencia
    lic_valid, info = check_license_online()
    if not lic_valid:
        show_activation_ui()
        # Re-validar tras cerrar la UI
        lic_valid, info = check_license_online()
        if not lic_valid: sys.exit(0)

    # 2. Activar entorno local para PHP
    os.makedirs(os.path.dirname(ATV_FILE), exist_ok=True)
    with open(ATV_FILE, "w") as f: f.write("1")
    
    # 3. Levantar Base de Datos y Apache
    if os.path.exists(SERVICE_BAT):
        subprocess.Popen([SERVICE_BAT], creationflags=subprocess.CREATE_NO_WINDOW, shell=True)
    
    # 4. Iniciar Servidor HTTP (Puerto 8876)
    threading.Thread(target=lambda: app.run(port=PORT_HTTP, host='0.0.0.0', use_reloader=False), daemon=True).start()
    
    # 5. Iniciar Watcher de Impresion
    temp_dir = os.path.join(BASE_DIR, "temp", "pos")
    os.makedirs(temp_dir, exist_ok=True)
    observer = Observer()
    observer.schedule(LegacyPrintHandler(), path=temp_dir, recursive=False)
    observer.start()
    
    print(f"Asistente ejecutándose. RIF: {info}")
    try:
        while True: time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()