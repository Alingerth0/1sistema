# Especificación Técnica V4: Nuevo POS Assistant (Portable)

## ... (Secciones 1 y 2 sin cambios) ...

## 5. Compilación y Distribución (Nuevo)

Para no instalar Python en el cliente, se usará **PyInstaller** para generar un ejecutable independiente.

### Requisitos previos (Solo en la PC del Desarrollador)
1.  Instalar Python 3.10 (32-bit recomendado para compatibilidad con DLLs antiguas).
2.  Instalar dependencias:
    ```cmd
    pip install -r requirements.txt
    pip install pyinstaller
    ```

### Estructura de Archivos para Compilación
```
/ProyectoPOS
  |-- main.py (El código fuente completo)
  |-- requirements.txt
  |-- build.bat (Script de compilación)
  |-- /dist (Aquí aparecerá el .exe final)
```

### Script de Compilación (`build.bat`)
Crea un archivo `.bat` con el siguiente contenido para automatizar el proceso:

```batch
@echo off
echo Compilando POS Assistant Portable...
pyinstaller --noconsole --onefile --clean ^
    --name "NewPOSAssistant" ^
    --hidden-import=win32timezone ^
    --add-data "requirements.txt;."
    main.py

echo.
echo Compilacion finalizada.
echo El archivo final esta en la carpeta: dist/NewPOSAssistant.exe
pause
```

### Instrucciones de Instalación en el Cliente
1.  Copiar `dist/NewPOSAssistant.exe` a la carpeta `D:\ESTO\1SISTEMA\pose\`.
2.  Asegurarse de que `IntTFHKA.exe` y las DLLs originales sigan en esa carpeta (el PHP las necesita).
3.  Crear un acceso directo al `.exe` en la carpeta "Inicio" (Startup) de Windows para que arranque solo.

## 6. Manejo de DLLs y Archivos Externos
Aunque el `.exe` contiene todo el Python necesario, el sistema sigue interactuando con archivos externos:
- **DLLs Fiscales:** No es necesario empaquetarlas *dentro* del exe. El script de Python las cargará desde la ruta relativa (la misma carpeta donde esté el exe).
- **IntTFHKA.exe:** Debe permanecer como archivo suelto junto al nuevo Assistant, ya que el código PHP legacy intenta ejecutarlo directamente.

---
*Documento generado por Gemini CLI - 19 de enero de 2026*