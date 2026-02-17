# RA3.2: Puesta en Producción Segura (DVWA)

## Descripción del Proyecto

Este repositorio contiene la documentación técnica y resolución práctica de la unidad **RA3.2: Ciberseguridad en entornos de las tecnologías de la información**.

El objetivo principal es desplegar un entorno de laboratorio controlado utilizando **Damn Vulnerable Web Application (DVWA)** para identificar, analizar y explotar vulnerabilidades web comunes (OWASP Top 10). A través de estas prácticas, se estudian los mecanismos de ataque y las contramedidas necesarias para asegurar las aplicaciones.

Todas las prácticas se han realizado cubriendo los niveles de dificultad **LOW** (Bajo) y **MEDIUM** (Medio), documentando el proceso de explotación, la metodología utilizada y las evidencias de éxito.

---

## Despliegue e Instalación

Para garantizar la reproducibilidad del entorno de laboratorio, se utiliza la tecnología de contenedores **Docker**. El servicio se expone en el puerto **9090** para evitar conflictos con otros servicios web del host.

### 1. Puesta en marcha del contenedor
Ejecutar el siguiente comando en la terminal para descargar la imagen oficial y arrancar el servidor:

```bash
docker run --rm -it -p 9090:80 vulnerables/web-dvwa

```

### 2. Acceso a la aplicación

Una vez iniciado el contenedor, acceder a través del navegador web utilizando la dirección IP del host:

```text
http://<TU_IP>:9090

```

*Nota: Se puede obtener la IP mediante el comando `ip a` (Linux) o `ipconfig` (Windows).*

### 3. Inicialización de Base de Datos

La primera vez que se accede al sistema, se redirigirá automáticamente a la pantalla de configuración (`/setup.php`).

1. Desplazarse al final de la página.
2. Pulsar el botón **Create / Reset Database**.
3. Esperar la redirección a la pantalla de inicio de sesión.

### 4. Credenciales de Acceso

* **Usuario:** `admin`
* **Contraseña:** `password`

---

## Entorno y Herramientas

* **Aplicación:** DVWA (Damn Vulnerable Web Application).
* **Navegador Recomendado:** **Mozilla Firefox**.
* **Justificación Técnica:** Firefox permite la manipulación de peticiones HTTP (Cabeceras y Cuerpo) de forma nativa mediante la función **"Edit and Resend"** en la pestaña de Red. Esto elimina la necesidad de proxies externos complejos para los niveles de dificultad media.


* **Herramientas Adicionales:** Herramientas de Desarrollador (F12), Terminal (para scripts Python).

---

## Gestión de Niveles de Seguridad

Para la realización de las prácticas es necesario alternar entre los niveles de seguridad **Low** y **Medium**.

### Método Estándar (Interfaz Web)

1. Navegar a la sección **DVWA Security** en el menú lateral.
2. Seleccionar el nivel deseado en el desplegable.
3. Pulsar **Submit**.

### Método Manual (Manipulación de Cookies)

En caso de fallo en la interfaz web, es posible forzar el cambio de nivel modificando la cookie de sesión directamente en el navegador.

1. Abrir las **Herramientas de Desarrollador** (F12).
2. Navegar a la pestaña **Storage** (Firefox) o **Application** (Chrome).
3. Desplegar la sección **Cookies** y seleccionar el dominio del servidor.
4. Localizar la cookie llamada `security`.
5. Modificar su valor manualmente:
* `low` (Para nivel bajo).
* `medium` (Para nivel medio).


6. Recargar la página para aplicar los cambios.

---

## Índice de Vulnerabilidades

A continuación se detalla el contenido de cada práctica. Haga clic en el enlace para acceder a la documentación específica.

### [1. Brute Force](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/01_brute_force)

Ataques de fuerza bruta para obtener credenciales de acceso mediante diccionarios y scripts personalizados en Python.

### [2. Command Injection](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/02_command_injection)

Ejecución arbitraria de comandos del sistema operativo a través de entradas no saneadas en la aplicación web.

### [3. CSP Bypass](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/03_csp_bypass)

Técnicas para eludir las Políticas de Seguridad de Contenido (Content Security Policy) y ejecutar scripts no autorizados.

### [4. CSRF (Cross-Site Request Forgery)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/04_csrf)

Falsificación de peticiones en sitios cruzados, forzando a un usuario autenticado a realizar acciones (como cambio de contraseña) sin su consentimiento.

### [5. XSS (DOM Based)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/05_xss_dom)

Explotación de vulnerabilidades Cross-Site Scripting basadas en la manipulación del Modelo de Objetos del Documento (DOM) en el cliente.

### [6. File Inclusion](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/06_file_inclusion)

Explotación de parámetros de archivo para leer ficheros sensibles del servidor local (LFI), como `/etc/passwd`.

### [7. File Upload](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/07_file_upload)

Subida de archivos maliciosos (Webshells PHP) al servidor eludiendo validaciones de tipo MIME.

### [8. JavaScript Attacks](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/08_javascript)

Manipulación de la lógica de seguridad del lado del cliente y generación manual de tokens criptográficos.

### [9. XSS (Reflected)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/09_xss_reflected)

Inyección de scripts maliciosos que se ejecutan inmediatamente al ser reflejados por el servidor en la respuesta HTTP.

### [10. SQL Injection (SQLi)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/10_sql_injection)

Inyección de código SQL en consultas a la base de datos para extraer listados completos de usuarios y contraseñas.

### [11. SQL Injection (Blind)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/11_sqli_blind)

Variante de SQLi donde la base de datos no devuelve datos visibles, requiriendo inferencia lógica (Booleana) para reconstruir la información.

### [12. XSS (Stored)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/12_xss_stored)

Inyección de scripts persistentes que se almacenan en la base de datos, afectando a cualquier usuario que visualice el contenido posteriormente.

### [13. Weak Session IDs](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3_2/13_weak_session)

Análisis estadístico de la generación de cookies de sesión para predecir identificadores y secuestrar sesiones activas.

---

## Aviso Legal (Disclaimer)

Este proyecto tiene fines estrictamente **educativos y académicos**. Las técnicas descritas se han realizado en un entorno de laboratorio controlado y aislado (DVWA). El uso de estas técnicas contra sistemas sin autorización explícita es ilegal.

---

**Autor:** Ruben Ferrer (brean-rb / 10813818)
