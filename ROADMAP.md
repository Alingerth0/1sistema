# Roadmap de Modernización y Refactoring

Este documento describe la estrategia para migrar el sistema POS Legacy (ThinkPHP 3.x / PHP 5) a una arquitectura moderna, segura y escalable.

## Fase 1: Estabilización y Seguridad (Inmediato)
*Objetivo: Asegurar la operación actual sin reescribir el núcleo.*

- [x] **Auditoría de Código:** Identificar vulnerabilidades críticas (completado).
- [ ] **Parcheo de Seguridad:** Eliminar backdoors y hardcoded credentials en `PublicAction.class.php`.
- [ ] **Dockerización:** Crear un `Dockerfile` que replique el entorno PHP 5.6/Apache para eliminar la dependencia de `1SS` portable y permitir despliegue en Linux/Cloud.
- [ ] **Sanitización de Inputs:** Implementar validación estricta en `ApiAction.class.php` para prevenir inyección SQL y XSS.

## Fase 2: Desacoplamiento (Corto Plazo)
*Objetivo: Separar el Frontend del Backend para facilitar la migración gradual.*

- [ ] **API Wrapper:** Crear una capa de rutas en el sistema actual que exponga JSON limpio, separando la vista (`display()`) de la lógica de datos.
- [ ] **Extracción de Lógica Fiscal:** Mover la lógica de generación de archivos TXT para impresoras fiscales a una clase/servicio independiente (Patrón Adaptador).
- [ ] **Documentación de API:** Documentar los endpoints actuales (`api_pos_ini`, `index_view`) usando Swagger/OpenAPI.

## Fase 3: Migración de Backend (Medio Plazo)
*Objetivo: Mover la lógica de negocio a un framework moderno (Laravel 10+).*

- [ ] **Migración de BD:** Crear migraciones de Laravel que repliquen el esquema actual (`pos_xs`, `pos_product`, etc.).
- [ ] **Modelos Eloquent:** Reemplazar los arrays asociativos de ThinkPHP (`M('Xs')->add($arr)`) por modelos tipados (`Sale::create($data)`).
- [ ] **Reescritura de Controladores:**
    - Migrar `IndexAction` (Ventas) -> `SalesController`.
    - Migrar `AdminAction` (Inventario) -> `InventoryController`.
- [ ] **Autenticación:** Implementar Laravel Sanctum o Passport, reemplazando el sistema de sesiones basado en archivos y MD5.

## Fase 4: Migración de Frontend (Largo Plazo)
*Objetivo: Reemplazar jQuery/HTML estático por una SPA reactiva.*

- [ ] **Tecnología:** Vue.js 3 o React.
- [ ] **Componentes:**
    - Crear componente `<PointOfSale />` que maneje el estado del carrito localmente (Pinia/Redux).
    - Crear componente `<FiscalStatus />` para monitorear la impresora.
- [ ] **Offline-First:** Implementar Service Workers y IndexedDB para permitir facturación sin internet, sincronizando cuando haya conexión (reemplazando la lógica actual de SQLite/Archivos).

## Estrategia de Base de Datos
Dado que el sistema tiene datos históricos:
1.  Mantener la base de datos MariaDB actual.
2.  Usar el nuevo backend para leer/escribir en las mismas tablas inicialmente.
3.  Eventualmente, normalizar el esquema (ej. separar `pos_xsy` en `users` y `roles`).

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
