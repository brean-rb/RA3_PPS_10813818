# Task 6: Nginx Secure Server

En esta última tarea, replicamos las prácticas de endurecimiento (Hardening) utilizando **Nginx**. El objetivo es demostrar que los principios de seguridad —como el cifrado SSL, la minimización de información y las cabeceras estrictas— son universales y aplicables independientemente de la tecnología del servidor web.

Esta imagen es **independiente** (standalone) y no hereda de las imágenes de Apache anteriores.

## 📂 Estructura del Directorio

A diferencia de Apache, Nginx centraliza su configuración en bloques de servidor. La estructura es la siguiente:

```text
task_6_nginx/
├── conf/
│   └── default.conf            # Configuración endurecida (Sobrescribe la default)
├── ssl/
│   ├── nginx.crt               # Certificado SSL
│   └── nginx.key               # Clave Privada
├── Dockerfile                  # Construcción de la imagen
└── README.md                   # Documentación técnica
```

---

## 🛠️ Configuración Técnica

### 1. Configuración Endurecida (`conf/default.conf`)
Este archivo es el corazón de la seguridad en Nginx. Reemplazamos la configuración por defecto para inyectar nuestras directivas de seguridad directamente en el bloque `server`.

```nginx
server {
    listen 443 ssl;
    server_name localhost;

    # Certificados SSL
    ssl_certificate /etc/nginx/ssl/nginx.crt;
    ssl_certificate_key /etc/nginx/ssl/nginx.key;
    ssl_protocols TLSv1.2 TLSv1.3;

    # 1. HARDENING DE INFORMACIÓN
    # Evita que Nginx muestre su número de versión en cabeceras y errores.
    server_tokens off;

    # 2. CABECERAS DE SEGURIDAD (Security Headers)
    # HSTS: Fuerza conexiones seguras.
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains" always;
    # Anti-Clickjacking.
    add_header X-Frame-Options "SAMEORIGIN";
    # XSS Protection.
    add_header X-XSS-Protection "1; mode=block";
    # Content Security Policy (CSP).
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'none';";

    # 3. CONTROL DE MÉTODOS (Whitelisting)
    # Bloqueamos cualquier método que no sea GET, HEAD o POST devolviendo un 405.
    if ($request_method !~ ^(GET|HEAD|POST)$ ) {
        return 405;
    }

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }
}

# Redirección de HTTP a HTTPS
server {
    listen 80;
    server_name localhost;
    return 301 https://$host$request_uri;
}
```

### 2. Dockerfile
El archivo de construcción es sencillo: parte de la imagen oficial de Nginx, inyecta las claves criptográficas y sustituye el archivo de configuración por defecto.

```dockerfile
# Usamos la imagen oficial ligera
FROM nginx:latest

# Herramientas de depuración
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copia de credenciales SSL
RUN mkdir -p /etc/nginx/ssl
COPY ssl/nginx.key /etc/nginx/ssl/
COPY ssl/nginx.crt /etc/nginx/ssl/

# Inyección de configuración segura
COPY conf/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
```

---

## 🚀 Despliegue y Validación

### Construcción Manual
```bash
# Construir la imagen
docker build -t pps/pr6 .

# Ejecutar contenedor (Puertos 8084/8447 para no colisionar con Apache)
docker run -d -p 8084:80 -p 8447:443 --name nginx_extra pps/pr6
```

### Validación de Seguridad
Utilizamos `curl` para inspeccionar las cabeceras HTTP que devuelve el servidor. Buscamos confirmar que la versión está oculta y las cabeceras de seguridad están presentes.

**Comando:**
```bash
curl -I -k https://localhost:8447
```

**Resultado Esperado:**
* `Server: nginx` (Sin números de versión como 1.25.x).
* Presencia de `Strict-Transport-Security`, `X-Frame-Options`, etc.

**Evidencia:**
![Validación Nginx](../asset/06_validacion_nginx.png)

---

## ☁️ DockerHub

Imagen pre-construida disponible para despliegue rápido:

```bash
docker pull brean19/pps-pr6:latest
```
