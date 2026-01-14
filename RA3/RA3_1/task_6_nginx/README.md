# Task 6: Nginx Secure Server

En esta última tarea, replicamos las prácticas de endurecimiento (Hardening) en un servidor **Nginx**. El objetivo es demostrar que los principios de seguridad (SSL, ocultación de información, cabeceras estrictas) son universales, independientemente de la tecnología del servidor web.

Esta imagen es **independiente** (standalone) y no hereda de las imágenes de Apache anteriores.

## 🎯 Objetivos de Seguridad

1.  **Cifrado SSL/TLS:** Generación de certificados y configuración de bloque `server` en puerto 443.
2.  **Hardening de Información:** Ocultación de la versión del servidor mediante `server_tokens off`.
3.  **Cabeceras de Seguridad:** Implementación manual de HSTS, CSP, X-Frame-Options y X-XSS-Protection.
4.  **Control de Métodos:** Bloqueo de cualquier método HTTP que no sea GET, HEAD o POST.

## 📂 Estructura de Archivos

* `Dockerfile`: Basado en la imagen oficial `nginx:latest`, inyecta nuestra configuración personalizada.
* `conf/default.conf`: Archivo crítico que sobrescribe la configuración por defecto de Nginx con las directivas de seguridad.
* `ssl/`: Almacén de claves criptográficas.

## 🛠️ Procedimiento de Construcción

### 1. Configuración Endurecida (default.conf)
A diferencia de Apache, en Nginx centralizamos la seguridad en el bloque del servidor:

```nginx
# Ocultar versión
server_tokens off;

# Cabeceras de Seguridad
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'none';";

# Bloqueo de métodos (Whitelisting)
if ($request_method !~ ^(GET|HEAD|POST)$ ) {
    return 405;
}

```

### 2. Dockerfile

El proceso de construcción copia los certificados y reemplaza la configuración por defecto:

```dockerfile
FROM nginx:latest
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY ssl/nginx.key /etc/nginx/ssl/

```

### 3. Docker Build & Run

Comandos utilizados para generar la imagen:

```bash
# Construir imagen (Etiqueta pr6)
docker build -t pps/pr6 .

# Ejecutar contenedor (Puertos 8084->80, 8447->443)
docker run -d -p 8084:80 -p 8447:443 --name nginx_extra pps/pr6

```

## ✅ Validación

Se utiliza `curl` para inspeccionar las cabeceras de respuesta del servidor Nginx.

**Comando:**

```bash
curl -I -k https://localhost:8447

```

**Resultado esperado:**

* `Server: nginx` (Sin número de versión).
* Presencia de `Strict-Transport-Security` y `X-Frame-Options`.

**Evidencia:**

## ☁️ DockerHub

![Validación Nginx](../asset/06_validacion_nginx.png)

La imagen está disponible públicamente:

```bash
docker pull brean19/pps-pr6:latest

```

