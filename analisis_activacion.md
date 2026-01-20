# Análisis del Sistema de Activación y Claves

Este documento detalla el funcionamiento lógico de la "Activación" del sistema POS, basado en la ingeniería inversa del código fuente (`PublicAction.class.php`, `pos_atv.html` y `common.php`).

## 1. Mecanismo de Activación (`pos_atv`)
El sistema cuenta con una pantalla de activación que solicita: Empresa, RIF, Tienda, Caja y **Código de Activación**.

### Hallazgos Críticos
- **Validación Nula:** La función encargada de procesar este formulario es `pos_atv_now` en `PublicAction.class.php`.
    ```php
    public function pos_atv_now(){
        $pos = M('Pos');
        if ($pos->create()){
            // Guarda DIRECTAMENTE lo que envía el usuario sin verificar el código
            $list = $pos -> where('id =1')-> save();
            if ($list !== false) {
                file_put_contents('welcome.txt', $_POST['caja']);
                $this->ajaxReturn(1,'1',1);
            }
            // ...
        }
    }
    ```
- **Conclusión:** El sistema **NO valida** que el "Código de Activación" corresponda a una fórmula matemática basada en el RIF o Serial. Simplemente guarda lo que el usuario escriba. Es un campo de registro, no de seguridad criptográfica en el backend.

## 2. Claves y PINs Encontrados
Durante la auditoría se encontraron referencias a códigos hardcodeados (fijos) en el código:

| Contexto | Clave / Código | Archivo | Función |
| :--- | :--- | :--- | :--- |
| **PIN de Verificación** | `2013` | `PublicAction.class.php` | `pin_ck()` |
| **Backdoor Admin** | `admin888` (Hash MD5) | `PublicAction.class.php` | `checklogin` |
| **Generador Aleatorio** | N/A (Aleatorio) | `common.php` | `genz()` |

### El PIN "2013"
Existe una función específica que valida un PIN ingresado por el usuario:
```php
public function pin_ck(){
    $pin = $_POST['pin'];
    if ($pin == '2013'){
        $this->ajaxReturn('1','1',1);
    } // ...
}
```
Es muy probable que este sea el código requerido para acceder a menús protegidos o desbloquear ciertas funciones de configuración inicial.

## 3. Archivos de Control
- **`welcome.txt`:** Almacena el número de caja (ej. "01", "02"). Es escrito por `pos_atv_now`.
- **`atv.txt`:** Ubicado en `data/config/atv.txt`. El sistema lee este archivo al inicio (`PublicAction::index`), pero no se encontró código PHP que escriba en él. Si este archivo contiene un "1", es posible que el sistema se considere "activado" globalmente.

## 4. Conclusión Técnica
Si el sistema te pide un "código de activación":
1.  **Cualquier código debería funcionar** si el formulario es procesado por `pos_atv_now`, ya que no hay `if ($code == $valid_code)` en el PHP.
2.  Si te pide un **PIN** de acceso, prueba con **`2013`**.
3.  La "seguridad" de la licencia reside en la oscuridad (no saber cómo funciona) más que en criptografía real.

## 5. POS Assistant y Validación Manual
El usuario reporta el uso de un programa externo `POS Assistant.exe`.

### Rol de POS Assistant
- Es un ejecutable compilado (no PHP) que corre en paralelo.
- Probablemente lee la base de datos (`pos_set`) y verifica si el `activation_code` coincide con el `rif` usando un algoritmo propietario.
- Si la validación es exitosa, escribe en archivos de bandera o actualiza la BD.

### Cómo "Validar" Manualmente (Bypass)
Dado que no tenemos el algoritmo del EXE para generar un código válido, la solución es simular que la validación ya ocurrió.

1.  **Archivo `welcome.txt`:** Asegúrese de que contenga el número de caja (ej. `01`). Ubicación: `1SISTEMA\pose\welcome.txt`.
2.  **Archivo `atv.txt`:** Crear o editar `1SISTEMA\pose\data\config\atv.txt` y escribir el contenido `1`. Esto suele indicarle al sistema web que está "Activado".
3.  **Base de Datos:** En la tabla `pos_set`, el campo `activation_code` puede contener cualquier valor si se realizan los pasos anteriores, ya que el PHP no lo verifica matemáticamente.

## 6. Relación POS Assistant - Base de Datos
El usuario reporta que "Si POS Assistant no funciona, no conecta a la DB".

### Explicación Técnica
El sistema de base de datos (MariaDB) y el servidor web (Apache) son servicios independientes ubicados en la carpeta `1SS`.
- **Comportamiento Normal:** Probablemente `POS Assistant.exe` ejecuta el script de inicio (`1SS\1.bat`) al abrirse. Por eso, si no abres el Assistant, los servicios no arrancan y ves un error de conexión.
- **Solución (Bypass):** Puedes iniciar los servicios **sin** abrir POS Assistant ejecutando manualmente el archivo:
    `D:\ESTO\1SS\1.bat`
    
    Esto levantará Apache y MySQL (MariaDB) permitiéndote entrar al sistema web (localhost/pose) incluso si POS Assistant está cerrado (aunque la impresión fiscal no funcionará).

---
*Documento generado por Gemini CLI - 19 de enero de 2026*
