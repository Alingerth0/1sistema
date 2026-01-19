# Análisis del Proyecto: Sistema POS Legacy (ThinkPHP)

## 1. Resumen Ejecutivo
Este es un sistema de **Punto de Venta (POS)** web empaquetado como aplicación de escritorio para Windows. Utiliza un entorno portable para ejecutar servicios web de forma local.

## 2. Tecnologías Identificadas
- **Lenguaje:** PHP 5.x (Legacy).
- **Framework:** ThinkPHP 3.x (Framework MVC popular en China).
- **Servidor Web:** Apache 2.x (Localizado en `1SS\server\Apache2`).
- **Base de Datos:** MariaDB/MySQL (Localizado en `1SS\server\MariaDB`).
- **Frontend:** HTML, CSS, JavaScript (Localizados en `1SISTEMA\pose\skin` y `1SISTEMA\pose\pose\Tpl`).
- **Interoperabilidad:** Archivos `.dll` (BemaFI32, tfhkaif) para comunicación con impresoras fiscales y periféricos.

## 3. Estructura de Directorios Clave
- `1SISTEMA\pose\`: Raíz de la aplicación web.
    - `index.php`: Punto de entrada principal.
    - `Core\`: Núcleo del framework ThinkPHP.
    - `pose\`: Directorio de la aplicación personalizada (MVC).
        - `Conf\`: Configuraciones globales.
        - `Lib\`: Lógica de negocio (Controladores y Modelos).
        - `Tpl\`: Plantillas de la interfaz (Vistas).
    - `skin\`: Activos estáticos (Imágenes, CSS, JS del tema).
- `1SS\`: Servidor portable (Apache, MariaDB, PHP).
- `1SISTEMA\sql\`: Gestión de BD (posiblemente phpMyAdmin).

## 4. Arquitectura de la Aplicación (MVC)
El proyecto sigue el patrón Modelo-Vista-Controlador de ThinkPHP:

### Vistas (Interfaz de Usuario)
Ubicación: `D:\ESTO\1SISTEMA\pose\pose\Tpl\`
- **`Admin\`**: Interfaz del panel de administración/backend.
- **`Index\`**: Interfaz principal del punto de venta (Caja).
- **`Pub\` / `Public\`**: Fragmentos reutilizables (headers, footers, menús).

### Lógica (Backend)
Ubicación: `D:\ESTO\1SISTEMA\pose\pose\Lib\`
- **`Action\`**: Controladores (Manejan las peticiones del usuario).
- **`Model\`**: Modelos (Interacción con tablas de la base de datos).

## 5. Configuración Crítica (Base de Datos)
Extraída de: `1SISTEMA\pose\pose\Conf\db.php`

### Credenciales Principales (MySQL/MariaDB)
| Parámetro | Valor |
| :--- | :--- |
| **Tipo** | MySQL |
| **Host** | `localhost` |
| **Puerto** | `3306` |
| **Base de Datos** | `pose` |
| **Usuario** | `root` |
| **Contraseña** | `123456` |
| **Prefijo Tablas** | `pos_` |

### Notas Adicionales
- **SQLite:** Se encontró configuración para una base de datos secundaria (`pos.s3db`), lo que sugiere capacidad de funcionamiento offline o un mecanismo de respaldo local.

## 6. Lógica de Negocio Detallada (Ingeniería Inversa)

### Facturación Fiscal (TheFactory / HKA)
- **Mecanismo:** Basado en archivos de texto ("File Spooling"). PHP no habla directo con la impresora.
- **Proceso:** 
    1. PHP genera un archivo `.txt` en `temp/fiscal_log/`. 
    2. El archivo contiene comandos fiscales (Ej: `iS*Cliente`, `!Ticket`).
    3. Un ejecutable externo (`IntTFHKA` o similar) monitorea la carpeta, lee el archivo y lo envía al hardware.
- **Validación:** Existe un bloqueo de seguridad si el total calculado difiere del total de la venta en más de 10 unidades monetarias.

### Sistema de Descuentos
- **Cálculo:** Se almacenan como factor multiplicador (Ej: 20% descuento -> se guarda `0.8`).
- **Seguridad:** Requiere validación de permisos (`passwd_fun_on`) antes de aplicar cambios en la BD.

### Sincronización (Cadenas)
- **Método:** Envío de JSON vía HTTP POST a un servidor central (`$pos_set['server']`) cada vez que se procesa el inventario.

## 7. Viabilidad de Edición
- **Lógica Web:** 100% editable (Archivos .php, .js, .html).
- **Entorno:** Configurable mediante archivos `.ini` y `.conf`.
- **Restricciones:** Los archivos ejecutables (`.exe`) y librerías compiladas (`.dll`) no pueden modificarse sin ingeniería inversa.

---
*Documento actualizado por Gemini CLI - 19 de enero de 2026
