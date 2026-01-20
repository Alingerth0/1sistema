# Manual Maestro de Ejecución y Despliegue

Este documento centraliza toda la información técnica, operativa y de seguridad del proyecto POS Legacy actualizado.

## 1. Resumen del Proyecto
Sistema de Punto de Venta (POS) basado en PHP 5 y ThinkPHP, diseñado para ejecutarse en Windows de forma portable. Se ha desarrollado un "Nuevo POS Assistant" en Python para reemplazar el software original de control de hardware y licencias.

## 2. Claves y Accesos Secretos
Guarde esta información en un lugar seguro.

| Recurso | Usuario / Clave | Notas |
| :--- | :--- | :--- |
| **Login POS** | Usuario configurado | Si falla, usar método de recuperación de BD. |
| **PIN Maestro** | `2013` | Desbloquea menús protegidos en la caja. |
| **Base de Datos** | `root` / `123456` | Puerto 3306. |
| **Activación** | N/A | El sistema acepta cualquier código en el formulario `pos_atv`. |

## 3. Guía de Inicio Rápido (Legacy Manual)
Si necesita arrancar el sistema **sin** el nuevo asistente (modo emergencia):

1. Vaya a la carpeta `D:\ESTO\1SS\`.
2. Ejecute `1.bat`. Esto enciende Apache y MySQL.
3. Abra su navegador en `http://localhost/pose`.
4. Si pide activación, ingrese cualquier código.
5. Asegúrese de que exista el archivo `D:\ESTO\1SISTEMA\pose\data\config\atv.txt` con el contenido `1`.

## 4. Guía del Nuevo POS Assistant

### A. Preparación del Entorno (Desarrollador)
Para crear el ejecutable que se le dará al cliente:

1. Instale **Python 3.10** (versión 32-bit recomendada).
2. Abra una terminal en la carpeta del proyecto.
3. Instale librerías:
    ```cmd
    pip install -r requirements.txt
    pip install pyinstaller
    ```

### B. Compilación
1. Haga doble clic en el archivo `build_exe.bat`.
2. Espere a que termine el proceso.
3. El archivo final estará en `dist\NewPOSAssistant.exe`.

### C. Instalación en el Cliente
1. Copie `NewPOSAssistant.exe` a la carpeta `D:\1SISTEMA\pose\` (o donde resida la aplicación en el cliente).
2. **IMPORTANTE:** Renombre la impresora de tickets en Windows a **`IMP1`**.
3. Cree un acceso directo de `NewPOSAssistant.exe` y póngalo en la carpeta "Inicio" de Windows (`shell:startup`).
4. Ejecute `NewPOSAssistant.exe`. Esto automáticamente:
    *   Validará la licencia (actualmente en modo bypass).
    *   Arrancará la base de datos (`1SS\1.bat`).
    *   Activará la escucha de impresión.

## 5. Solución de Problemas Frecuentes

### "Error de conexión a la Base de Datos"
*   **Causa:** `mysqld.exe` no se está ejecutando.
*   **Solución:** Abra `NewPOSAssistant.exe`. Si no abre, ejecute manualmente `D:\ESTO\1SS\1.bat`.

### "No imprime el ticket"
*   **Causa:** La impresora no se llama `IMP1` o el asistente no está corriendo.
*   **Solución:** Verifique en "Dispositivos e Impresoras" que el nombre sea exacto. Verifique que la consola negra del Assistant no tenga errores rojos.

### "Pide código de activación constantemente"
*   **Causa:** El archivo `atv.txt` no se puede escribir o se borra.
*   **Solución:** Revise permisos de escritura en la carpeta `data/config/`. Cree el archivo manualmente con un `1` adentro.

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
