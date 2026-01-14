# Task 1: Apache Base Hardening + SSL

Esta carpeta contiene la configuración inicial para un servidor Apache seguro. Es la **imagen base** sobre la que se construirán las siguientes capas del proyecto.

## 🎯 Objetivos de Seguridad

1.  **Cifrado (SSL/TLS):** Generación de certificados y configuración de VirtualHost en puerto 443.
2.  **Ocultación de Información:** Eliminación de la versión del servidor (`ServerTokens`) y firma (`ServerSignature`).
3.  **Cabeceras de Seguridad (Headers):**
    * **HSTS:** Fuerza conexiones seguras.
    * **CSP:** Política de seguridad de contenidos.
    * **X-XSS-Protection:** Bloqueo de Cross-Site Scripting básico.

## 📂 Estructura de Archivos

* `Dockerfile`: Construcción de la imagen basada en Debian.
* `ssl/`: Contiene el certificado (`apache.crt`) y la clave (`apache.key`) autofirmados.
* `conf/user-hardening.conf`: Directivas de hardening y cabeceras.
* `conf/default-ssl.conf`: Configuración del VirtualHost HTTPS.

## 🛠️ Procedimiento de Construcción

### 1. Certificados SSL
Se han generado certificados autofirmados válidos por 365 días:
```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout ssl/apache.key -out ssl/apache.crt

```

### 2. Configuración Hardening

Contenido clave de `conf/user-hardening.conf`:

```apache
ServerTokens Prod
ServerSignature Off
Header always set Strict-Transport-Security "max-age=63072000; includeSubDomains"
Header set Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; object-src 'none';"

```

### 3. Docker Build & Run

Comandos utilizados para generar y probar la imagen:

```bash
# Construir imagen
docker build -t pps/pr1 .

# Ejecutar contenedor (Mapeo puertos 8080->80, 8443->443)
docker run -d -p 8080:80 -p 8443:443 --name apache_task1 pps/pr1

```

## ✅ Validación

Se verifica la respuesta del servidor mediante `curl`. Se observa que la versión de Apache está oculta y las cabeceras de seguridad están presentes.

**Comando:**

```bash
curl -I -k https://localhost:8443

```

**Evidencia:**
![Validación Base](../asset/01_validacion_base.png)

## ☁️ DockerHub

La imagen está disponible públicamente:

```bash
docker pull brean19/pps-pr1:latest

```


