# RA3.1 - Apache Hardening

En esta práctica realizaremos el endurecimiento (hardening) de un servidor Apache y una implementación en Nginx, utilizando una estrategia de contenedores Docker progresivos (Layered Builds).

Este documento cubre los requisitos de las prácticas 3.1 (Hardening), 3.2 (Certificados) y 3.3 (Best Practices).

# Tasks

* [Task 1: Base Hardening + SSL (Prácticas 3.1.1 y 3.2)](#task_1)
* [Task 2: Web Application Firewall (Práctica 3.1.2)](#task_2)
* [Task 3: Reglas OWASP (Práctica 3.1.3)](#task_3)
* [Task 4: Protección Anti-DoS (Práctica 3.1.4)](#task_4)
* [Task 5: Hardening Extra (Práctica 3.3)](#task_5)
* [Task 6: Nginx Secure Server (Práctica 3.1.5)](#task_6)

---

# Task_1
**Objetivo:** Configuración base segura, ocultación de versión, certificados SSL y cabeceras HSTS/CSP. Se prioriza SSL para habilitar HSTS.

### Procedimiento
1. Generación de certificados autofirmados con OpenSSL (RSA 2048).
2. Configuración de Apache: `ServerTokens Prod` y `ServerSignature Off`.
3. Implementación de cabeceras estrictas: HSTS (2 años) y CSP.

### Validación
El servidor responde con HTTPS, oculta su versión y muestra las cabeceras de seguridad.

![Validación Headers](./asset/01_validacion_base.png)

### Código de Construcción

```bash
# Pull desde DockerHub
docker pull brean19/pps-pr1:latest

# Build manual (si se requiere)
cd task_1_base_ssl
docker build -t pps/pr1 .

```

---

# Task_2

**Objetivo:** Implementar un Firewall de Aplicación Web (ModSecurity) en modo bloqueo.

### Procedimiento

1. Instalación de `libapache2-mod-security2`.
2. Cambio de configuración de `DetectionOnly` a `On` en `modsecurity.conf`.
3. Herencia directa de la imagen de la Task 1.

### Validación

Al intentar un ataque XSS simple (`<script>alert(1)</script>`), el WAF bloquea la petición con un 403 Forbidden.

![Bloqueo WAF](./asset/02_validacion_waf.png)

### Código de Construcción

```bash
docker pull brean19/pps-pr2:latest

```

---

# Task_3

**Objetivo:** Integrar el **OWASP Core Rule Set (CRS)** para proteger contra inyecciones SQL y Path Traversal.

### Procedimiento

1. Descarga automática de las reglas OWASP CRS desde GitHub en el Dockerfile.
2. Configuración de Apache para incluir `crs-setup.conf` y `rules/*.conf`.

### Validación

Se bloquean intentos de Command Injection (`/bin/bash`) y Path Traversal (`../../etc/passwd`).

![Bloqueo OWASP](./asset/03_validacion_owasp.png)

### Código de Construcción

```bash
docker pull brean19/pps-pr3:latest

```

---

# Task_4

**Objetivo:** Mitigar ataques de Denegación de Servicio (DoS) usando `mod_evasive`.

### Procedimiento

1. Instalación del módulo `mod_evasive`.
2. Configuración de umbrales estrictos (`DOSPageCount 2`) para detección rápida.
3. Creación de directorio de logs con permisos para `www-data`.

### Validación

Prueba de estrés con `Apache Bench` (100 peticiones). El servidor bloquea 94 de ellas (`Failed requests`), baneando la IP atacante.

![Validación DoS](./asset/04_validacion_dos.png)

### Código de Construcción

```bash
docker pull brean19/pps-pr4:latest

```

---

# Task_5

**Objetivo:** Hardening avanzado basado en guías de mejores prácticas (Geekflare).

### Procedimiento

1. Reducción del `Timeout` a 60s.
2. Desactivación de métodos HTTP peligrosos (TRACE, OPTIONS).
3. Aseguramiento de Cookies con flags `HttpOnly` y `Secure`.

### Validación

El servidor rechaza métodos no permitidos (como OPTIONS) con un error 403.

![Validación Hardening](./asset/05_validacion_hardening.png)

### Código de Construcción

```bash
docker pull brean19/pps-pr5:latest

```

---

# Task_6

**Objetivo:** Implementación de seguridad equivalente en servidor Nginx.

### Procedimiento

1. Generación de certificados SSL específicos para Nginx.
2. Configuración de `server_tokens off`.
3. Inyección manual de cabeceras de seguridad (`add_header`) en `default.conf`.

### Validación

Nginx sirve contenido seguro, ocultando versión y aplicando HSTS/CSP.

![Validación Nginx](./asset/06_validacion_nginx.png)

### Código de Construcción

```bash
docker pull brean19/pps-pr6:latest

```



