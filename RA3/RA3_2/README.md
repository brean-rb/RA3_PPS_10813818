# RA3.2: Puesta en Producción Segura (DVWA)

## 📖 Descripción del Proyecto

Este repositorio contiene la resolución práctica de la unidad **RA3.2: Ciberseguridad en entornos de las tecnologías de la información**.

El objetivo principal es desplegar un entorno controlado utilizando **Damn Vulnerable Web Application (DVWA)** para identificar, analizar y explotar vulnerabilidades web comunes. A través de estas prácticas, se estudian los mecanismos de ataque y, lo más importante, se comprende cómo asegurar las aplicaciones frente a ellos.

Todas las prácticas se han realizado cubriendo los niveles de dificultad **LOW** (Bajo) y **MEDIUM** (Medio), documentando el proceso de explotación, los payloads utilizados y las evidencias de éxito.

---

## 🚀 Despliegue e Instalación

Para replicar este entorno de laboratorio, utilizaremos **Docker**. Usaremos el puerto **9090** para evitar conflictos con otros servicios web que puedas tener en el puerto 80.

### 1. Puesta en marcha del contenedor
Ejecuta el siguiente comando en tu terminal para descargar la imagen y arrancar el servidor:

```bash
docker run --rm -it -p 9090:80 vulnerables/web-dvwa

```

### 2. Acceso a la aplicación

Una vez iniciado el contenedor, abre tu navegador web (preferiblemente **Firefox**).

* **Averigua tu IP:** Ejecuta el comando `ip a` (en Linux) o `ipconfig` (en Windows).
* **Accede a la URL:** Introduce tu IP seguida del puerto definido:
```text
http://<TU_IP>:9090

```

### 3. Configuración Inicial (Importante)

La primera vez que entres, serás redirigido a la pantalla de configuración (`/setup.php`).

1. Baja hasta el final de la página.
2. Pulsa el botón **Create / Reset Database**.
3. Espera unos segundos hasta que te redirija a la pantalla de Login.

### 4. Credenciales de Acceso

Utiliza las credenciales por defecto para iniciar sesión:

* **Usuario:** `admin`
* **Contraseña:** `password`

---

## 🛠️ Entorno y Herramientas

* **Aplicación:** DVWA (Damn Vulnerable Web Application) desplegada en servidor local (Docker/XAMPP).
* **Navegador Recomendado:** **Mozilla Firefox**.
    * *Motivo:* Facilita enormemente la manipulación de peticiones HTTP mediante la función nativa **"Edit and Resend"** en la pestaña de Red, algo vital para los niveles Medium.
* **Herramientas Adicionales:** Herramientas de Desarrollador (F12), Burp Suite (opcional), Terminal.

---

## ⚙️ Gestión de Niveles de Seguridad (IMPORTANTE)

Para realizar estas prácticas es necesario alternar entre los niveles de seguridad **Low** y **Medium**. Existen dos formas de hacerlo:

### 1. Método Estándar (Interfaz Web)
1.  En el menú lateral izquierdo, ve a **DVWA Security**.
2.  En el desplegable "Security Level", selecciona **Low** o **Medium**.
3.  Pulsa el botón **Submit**.
4.  Verifica que abajo a la izquierda aparece: `Security Level: Low` (o Medium).

### 2. Método "Hacker" (Modificación de Cookies)
*Utiliza este método si la interfaz web falla, se queda bloqueada o no aplica los cambios correctamente.*

1.  Abre las **Herramientas de Desarrollador** (F12).
2.  Ve a la pestaña **Storage** (Firefox) o **Application** (Chrome).
3.  En el menú lateral, despliega **Cookies** y selecciona la URL de tu servidor (`http://192.168...`).
4.  Busca la cookie llamada **`security`**.
5.  Haz doble clic en su valor (Value) y escribe manualmente:
    * `low` (para nivel bajo).
    * `medium` (para nivel medio).
6.  Pulsa Enter y **recarga la página (F5)**.
7.  El nivel de seguridad habrá cambiado forzosamente.

---

## 📂 Índice de Vulnerabilidades

El repositorio está estructurado en carpetas individuales para cada tipo de vulnerabilidad. A continuación se detalla el contenido de cada una:

### 1. Brute Force
Ataques de fuerza bruta para adivinar credenciales de acceso mediante diccionarios o prueba y error automatizada.

### 2. Command Injection
Ejecución de comandos del sistema operativo (shell) a través de inputs no saneados en la aplicación web.

### 3. CSRF (Cross-Site Request Forgery)
Falsificación de peticiones en sitios cruzados, obligando a un usuario autenticado a realizar acciones sin su consentimiento (ej: cambiar su contraseña).

### 4. File Inclusion (LFI / RFI)
Explotación de parámetros de archivo para leer archivos sensibles del servidor local (LFI) o ejecutar scripts alojados remotamente (RFI).

### 5. File Upload
Subida de archivos maliciosos (webshells PHP) al servidor para tomar el control del mismo.
* **Nota:** En nivel Medium se requiere manipulación del `Content-Type` (MIME Type) de la petición.

### 6. JavaScript Attacks
Manipulación de la lógica de seguridad del lado del cliente.
* **Técnica:** Ingeniería inversa de funciones JS para generar tokens válidos y saltarse protecciones.

### 7. SQL Injection (SQLi)
Inyección de código SQL en consultas a la base de datos para extraer información confidencial (listas de usuarios y contraseñas).

### 8. SQL Injection (Blind)
Variante de SQLi donde la base de datos no devuelve datos visibles, sino respuestas de tipo Verdadero/Falso. Se utiliza lógica booleana para inferir la información.

### 9. XSS (Reflected)
Inyección de scripts maliciosos que se ejecutan inmediatamente al ser reflejados por el servidor.
* **Payload:** `<img src=x onerror=alert(...)>`

### 10. XSS (Stored)
Inyección de scripts persistentes que se guardan en la base de datos (ej: libros de visitas), afectando a cualquier usuario que visite la página posteriormente.

### 11. Weak Session IDs
Análisis de la generación de cookies de sesión para predecir y secuestrar sesiones de otros usuarios legítimos.

---

## ⚠️ Disclaimer

Este proyecto tiene fines estrictamente **educativos y académicos**. Las técnicas aquí descritas se han realizado en un entorno de laboratorio controlado y aislado (DVWA). El uso de estas técnicas contra sistemas sin autorización explícita es ilegal y éticamente incorrecto.

---
*Autor: Ruben Ferrer*

