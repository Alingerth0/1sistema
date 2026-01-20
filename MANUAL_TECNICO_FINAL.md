# Manual Técnico Final: Reemplazo POS Assistant

Este documento explica cómo mantener, compilar y desplegar el nuevo asistente.

## 1. Funcionamiento Lógico
El programa `NewPOSAssistant.exe` cumple 4 funciones críticas simultáneas:
1.  **Activación:** Verifica el RIF local contra un JSON en GitHub Pages. Si es válido, crea el archivo `data/config/atv.txt` que el PHP necesita para "sentirse" activado.
2.  **Servicios:** Al arrancar, ejecuta el archivo `1SS\1.bat` de forma invisible. Esto garantiza que la base de datos MySQL esté disponible.
3.  **Puente HTTP (Puerto 8876):** Escucha peticiones del sistema web para imprimir tickets o leer la balanza.
4.  **Monitor de Archivos:** Vigila la carpeta `temp/pos/` por si el PHP escribe archivos `.txt` de impresión (método antiguo).

## 2. Preparación para Nuevos Clientes
Para activar un sistema en un cliente nuevo:
1.  Obtén el **UUID** del cliente (el programa lo muestra en la consola o puedes usar `wmic csproduct get uuid` en CMD).
2.  Edita tu archivo `licencias.json` en tu repositorio GitHub:
    - Agrega el RIF del cliente.
    - Agrega el UUID en el campo `hwid`.
    - Define un `codigo_activacion` (ej: `CLAVE777`).
3.  En la primera ejecución del asistente en el cliente, ingresa el RIF y el Código.

## 3. Compilación del Ejecutable
Si realizas cambios en `main.py`, debes generar un nuevo `.exe`:
1.  Ejecuta `build_exe.bat`.
2.  Busca el archivo en `dist\NewPOSAssistant.exe`.
3.  **Peso aproximado:** ~10-15MB (incluye todo el entorno Python).

## 4. Estructura de Carpetas en el Cliente
El asistente debe estar ubicado en la raíz de la aplicación web:
```
D:\1SISTEMA\pose\
  |-- NewPOSAssistant.exe  <-- Tu programa
  |-- main.py              <-- Fuente (opcional)
  |-- rif.txt              <-- Creado tras la activacion
  |-- IntTFHKA.exe         <-- Mantener para drivers fiscales
  |-- /temp/pos/           <-- Donde caen los tickets
  |-- /data/config/atv.txt <-- Bandera de activacion
```

## 5. Datos Maestros
- **Puerto de Hardware:** 8876
- **PIN de Emergencia PHP:** 2013
- **Contraseña BD:** 123456 (Usuario root)

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
