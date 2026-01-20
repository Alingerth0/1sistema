@echo off
:: Script para compilar el POS Assistant en un solo EXE portable
:: Requiere: pip install pyinstaller

echo ==========================================
echo      COMPILANDO NUEVO POS ASSISTANT
echo ==========================================

:: Verificar si PyInstaller esta instalado
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: PyInstaller no esta instalado.
    echo Ejecuta: pip install pyinstaller
    pause
    exit /b
)

:: Limpiar compilaciones previas
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist *.spec del *.spec

:: Ejecutar compilacion
:: --noconsole: No muestra la ventana negra de comandos
:: --onefile: Crea un solo archivo .exe
:: --clean: Limpiara cache antes de compilar
pyinstaller --noconsole --onefile --clean ^
    --name "NewPOSAssistant" ^
    --hidden-import=win32timezone ^
    --hidden-import=flask ^
    --hidden-import=engineio.async_drivers.threading ^
    main.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo      COMPILACION EXITOSA
    echo ==========================================
    echo Tu archivo ejecutable esta en: dist\NewPOSAssistant.exe
    echo.
    echo Copia este archivo a la carpeta del sistema POS.
) else (
    echo.
    echo OCURRIO UN ERROR DURANTE LA COMPILACION.
)

pause
