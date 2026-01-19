# Auditoría Técnica del Sistema POS Legacy

## 1. Arquitectura del Sistema
El sistema está construido sobre una arquitectura **MVC (Modelo-Vista-Controlador)** utilizando el framework PHP **ThinkPHP 3.x**.

- **Entorno de Ejecución:**
  - Servidor Web: Apache 2.x (Portátil en `1SS\server\Apache2`)
  - Intérprete: PHP 5.x
  - Base de Datos: MariaDB (MySQL compatible)
  - Sistema Operativo: Windows (Dependencias de `.exe` y `.dll`)

- **Patrón de Diseño:**
  - **Controladores (`Action`):** `1SISTEMA\pose\pose\Lib\Action\` - Manejan la lógica de negocio.
  - **Modelos (`Model`):** Utiliza principalmente la clase `M()` de ThinkPHP para mapeo directo a tablas (`ActiveRecord` simple).
  - **Vistas (`Tpl`):** Archivos HTML con etiquetas de plantilla ThinkPHP.

## 2. Estructura de Base de Datos
Prefijo de tablas: `pos_`
Motor: MyISAM o InnoDB (basado en la presencia de archivos `.sql` de restauración).

### Tablas Principales Identificadas
| Tabla | Descripción | Campos Clave (Inferidos) |
| :--- | :--- | :--- |
| `pos_xs` | Cabecera de Ventas | `id`, `no` (número), `atv` (estado), `fecha`, `total`, `kh_id` (cliente), `xsy_id` (cajero) |
| `pos_xsmx` | Detalle de Ventas | `xs_id` (fk), `pid` (producto), `cant`, `precio`, `costo`, `iva` |
| `pos_kh` | Clientes | `id`, `no`, `name`, `rif`, `tel` |
| `pos_xsy` | Usuarios/Cajeros | `id`, `name`, `clave` (MD5), `tipo` (rol) |
| `pos_ck` | Inventario (Stock) | `pid` (producto), `cant`, `warehouse_id` |
| `pos_product` | Catálogo de Productos | `id`, `codigo`, `name`, `precio`, `costo`, `paquete` |
| `pos_jck` | Movimientos de Stock | `pid`, `cant`, `tipo`, `original_id` (referencia a venta) |
| `pos_archive_*` | Histórico | Tablas espejo (`archive_sales`, etc.) para ventas sincronizadas/cerradas |

## 3. Seguridad y Autenticación
### Hallazgos Críticos
- **Hash de Contraseñas:** Se utiliza **MD5** simple (`md5($_POST['clave'])`), lo cual es vulnerable a ataques de fuerza bruta hoy en día.
- **Backdoor / Clave Maestra:** Se identificó una comparación explícita en `PublicAction.class.php` con el hash `898e8cf672de502699dda5adbdee5c22`. Esto permite acceso privilegiado (`tipo = 1`) independientemente del usuario.
- **Validación de Sesión:** El controlador base `GateAction` verifica la existencia de `xsy_id` en la sesión. Si no existe, redirige al login.
- **Reset de Claves:** Función `reset_gen` restablece la clave del usuario ID 5 a un hash conocido (MD5 de '123456').

## 4. Integraciones y Periféricos
### Impresoras Fiscales
- **Método:** File Spooling (Cola de archivos).
- **Flujo:** PHP escribe archivos de texto en `temp/fiscal_log/` o `C:\IntTFHKA`. Un proceso externo (`IntTFHKA.exe`) lee estos archivos y comanda la impresora.
- **Drivers:** DLLs presentes en `1SISTEMA\pose\res\` (`tfhkaif.dll`).

### Sincronización
- **Método:** API REST ad-hoc (JSON sobre HTTP POST).
- **Endpoint:** `ApiAction.class.php` maneja la recepción de datos (`api_inventory_processing`).
- **Cliente:** `PublicAction::pos_update` descarga ZIPs desde un servidor central configurado en `pos_set`.

## 5. Procesos Críticos
- **Cierre y Mantenimiento (`maintain`):**
  - Elimina ventas pendientes (`atv` 0 o 2) con más de 7 días de antigüedad.
  - Elimina ventas ya sincronizadas (`sync` 1) con más de 30 días para ahorrar espacio.
  - Ejecuta `OPTIMIZE TABLE` y `REPAIR TABLE` automáticamente.
- **Restauración (`db_restore`):**
  - Utilidad integrada `MySQLReback` para importar dumps SQL completos o parciales.
  - El sistema verifica `version.txt` al inicio para aplicar parches de esquema de base de datos (`pos_update_db`).

## 6. Recomendaciones Inmediatas
1.  **Backup Completo:** Antes de cualquier cambio, ejecutar la herramienta de backup interna (`/index.php?s=/Public/db_all_back`).
2.  **Aislar el Entorno:** Dado el uso de PHP 5 y componentes legacy, evitar exponer este servidor directamente a Internet. Usar VPN si se requiere acceso remoto.
3.  **Sanitización:** Revisar `ApiAction` ya que recibe JSON crudo y lo pasa a métodos `M()->add()`. Aunque ThinkPHP 3 tiene cierta protección, validar los tipos de datos es crucial.

## 7. Análisis del Frontend (Interfaz de Caja)
Ubicación: `1SISTEMA\pose\skin\comm.js` y `Tpl\Index\`.

### Arquitectura de Cliente
- **Framework:** jQuery 1.8.2.
- **SPA Híbrida:** La aplicación carga una estructura base y manipula el DOM dinámicamente mediante AJAX, evitando recargas completas en el proceso de venta.
- **Estado Global:** Variables globales como `G_pos` (configuración), `G_set` (opciones) y `G_cart` mantienen el estado de la sesión en el navegador.

### Flujo de Interacción
1.  **Inicialización (`G()`):** Al cargar, llama a `api_pos_ini` para obtener configuración y permisos.
2.  **Renderizado:** La función `index_view` recibe JSON del servidor y construye el HTML de la lista de productos (carrito) concatenando strings de JS.
3.  **Teclado:** Mapeo directo de teclas de función (F1-F12) a funciones JS (`pos_kh()`, `pos_pay()`).

### Estilo
- **CSS:** Framework propio minimalista `uniui.css`. Diseño orientado a pantallas táctiles y teclado (botones grandes, alto contraste).

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
