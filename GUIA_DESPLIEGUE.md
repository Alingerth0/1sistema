# Guía de Despliegue y Ejecución (Entorno Legacy)

Este proyecto utiliza un entorno portable "WAMP" (Windows, Apache, MariaDB, PHP) pre-configurado para ejecutar el sistema POS.

## Requisitos del Sistema
- **Sistema Operativo:** Windows XP, 7, 10 u 11 (x86/x64).
- **Dependencias:** Librerías Visual C++ Redistributable (para PHP 5.x y Apache 2.x antiguas).
- **Puertos:**
    - Apache: 80 (HTTP)
    - MySQL/MariaDB: 3306

## Estructura del Servidor Portable (`1SS`)
El núcleo del servidor se encuentra en `D:\ESTO\1SS\`.
- `Apache2\`: Servidor web.
- `MariaDB\`: Motor de base de datos.
- `PHP5\`: Intérprete PHP (Versión 5.x).

## Pasos para Iniciar
1.  **Ubicación:** Asegúrese de que la carpeta del proyecto esté en una ruta sin espacios complejos (aunque el sistema parece relativo, es mejor prevenir).
2.  **Arrancar Servicios:**
    *   Ejecute `D:\ESTO\1SS\1.bat`.
    *   Este script inicia los procesos `httpd.exe` (Apache) y `mysqld.exe` (MariaDB).
3.  **Verificación:**
    *   Abra un navegador y vaya a `http://localhost/pose/`.
    *   Debería ver la pantalla de login del POS.

## Pasos para Detener
1.  Ejecute `D:\ESTO\1SS\0.bat`.
2.  Este script mata los procesos asociados (`taskkill`).

## Configuración Técnica
### Apache (`httpd.conf`)
Ubicado en `1SS\server\Apache2\conf\`.
- **DocumentRoot:** Apunta a `../../1SISTEMA` (o similar relativo).
- **Módulos:** `mod_rewrite` debe estar activo para las URLs amigables de ThinkPHP.

### PHP (`php.ini`)
Ubicado en `1SS\server\PHP5\`.
- **Short Open Tags:** Debe estar en `On` (`<? ?>`).
- **Extensiones:** `php_mysql.dll`, `php_gd2.dll`, `php_mbstring.dll` son requeridas.

### Base de Datos
- **Usuario:** `root`
- **Contraseña:** `123456`
- **Host:** `localhost` (Puerto 3306)

## Solución de Problemas Comunes
*   **Error 404/500:** Verifique que el archivo `.htaccess` en `1SISTEMA\pose\` exista y tenga las reglas de reescritura correctas.
*   **Base de datos no conecta:** Verifique si el puerto 3306 está ocupado por otra instalación de MySQL.
*   **Impresora Fiscal no responde:** Asegúrese de que `IntTFHKA.exe` se esté ejecutando y tenga permisos de administrador para escribir en los puertos COM/USB.

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
