# Capacidades y Funcionalidades del Sistema POS

Este documento detalla qué puede hacer el sistema basado en el análisis del código fuente (`IndexAction.class.php` y `AdminAction.class.php`).

## 1. Punto de Venta (Front-Office)
Controlado principalmente por `IndexAction`, permite operar la caja registradora.

### Gestión de Ventas
- **Proceso de Venta:** Búsqueda de productos, escaneo de códigos de barra, cálculo de totales. (`IndexAction::index_view`, `ApiAction::api_gd_save`)
- **Tipos de Pago:** Múltiples formas de pago (`pos_pay`, `api_pay`), incluyendo crédito (`factura_credito`).
- **Control de Precios:** Cambio manual de precios (`pos_precio`), precios al mayor (`pos_mayor`), descuentos (`pos_disc`).
- **Anulaciones:** Borrado de líneas (`pos_rdel`), anulación completa.
- **Clientes:** Selección y creación rápida de clientes en caja (`pos_kh`, `pos_kh_add`). Tabla: `pos_kh`.

### Facturación Fiscal (Crítico)
El sistema tiene integración nativa con impresoras fiscales (posiblemente venezolanas o panameñas por las siglas HKA/TheFactory).
- **Comandos Fiscales:** Reporte X y Z (`pos_fiscal_report`), reimpresión de documentos.
- **Drivers:** Funciones específicas para comunicarse con hardware (`hka_check`, `thefactory_s1`).
- **Manejo de Gaveta:** Apertura automática de cajón de dinero (`hka_gaveta`).
- **Implementación:** File Spooling hacia `IntTFHKA.exe` o escritura directa a puerto.

### Operaciones de Caja
- **Turnos:** Apertura y cierre de caja.
- **Seguridad:** Verificación de claves y permisos para operaciones sensibles (`pos_passwd_check`, `pos_qx_check`).

## 2. Administración (Back-Office)
Controlado por `AdminAction`, maneja la configuración y el inventario.

### Inventario y Catálogo
- **Productos:** Altas, bajas y modificaciones de productos (`cp_add`, `cp_edit`, `cp_del`). Tabla: `pos_product`.
- **Categorías:** Gestión de familias de productos (`cp_cat`).
- **Almacenes:** Gestión de múltiples ubicaciones o depósitos (`cp_wh` - Warehouse). Tabla: `pos_ck` (Stocks).
- **Etiquetas:** Impresión de códigos de barra (`cp_bq`).
- **Ajustes:** Movimientos de inventario y ajustes manuales.

### Reportes
- **Ventas:** Reportes de ventas por período.
- **Inventario:** Reporte de existencias y valoración (`inventory_report`).
- **Cierre:** Reportes de cierre de turno y fiscales.

### Configuración del Sistema
- **Usuarios:** Gestión de vendedores y permisos (`os_xs`). Tabla: `pos_xsy`.
- **Moneda:** Configuración de divisas (`os_currency`).
- **Base de Datos:** Herramientas de respaldo y restauración (`db_restore`, `database_ret`).

## 3. Mantenimiento y Herramientas Técnicas
Controlado por `PublicAction`.

- **Auto-Mantenimiento:** Función `maintain` limpia registros antiguos (Ventas pendientes > 7 días, Sincronizadas > 30 días).
- **Actualización:** Sistema de parches automáticos vía SQL (`pos_update_db`) basado en `version.txt`.
- **Sincronización:** Carga y descarga de paquetes ZIP (`pos_zip_remot`, `lusync`) para operación offline/online.
- **Diagnóstico:** Herramientas para resetear inventario (`reset_inv`), ventas (`reset_xs`) o reparar tablas (`sqlfix`).

## 4. Límites y Observaciones Técnicas
- **Arquitectura Monolítica:** La lógica está muy concentrada en pocos archivos grandes, lo que facilita ediciones rápidas pero dificulta la escalabilidad moderna.
- **Dependencia de Hardware:** Las funciones fiscales dependen de librerías DLL externas (`tfhkaif.dll`) que solo funcionan en Windows x86.
- **Modo Offline:** Existen rastros de sincronización o modos locales (`sqlite`), útil para cuando falla la red principal (si la hubiera).

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
