# RA3.1 - Apache & Nginx Hardening Project

Este repositorio documenta la implementación progresiva de medidas de seguridad (Hardening) sobre servidores web Apache y Nginx. El proyecto sigue una estrategia de **Layered Builds** (construcción por capas) en Docker, donde cada fase hereda y mejora la anterior.

Este documento consolida los requisitos de las prácticas **3.1 (Hardening)**, **3.2 (Certificados)** y **3.3 (Best Practices)**.

## 📂 Estructura del Proyecto

```text
RA3/
├── RA3_1
│   ├── asset/                      # Evidencias y capturas de validación
│   │   ├── 01_validacion_base.png
│   │   ├── 02_validacion_waf.png
│   │   ├── 03_validacion_owasp.png
│   │   ├── 04_validacion_dos.png
│   │   ├── 05_validacion_hardening.png
│   │   └── 06_validacion_nginx.png
│   ├── README.md                   # Documentación Principal (Este archivo)
│   ├── task_1_base_ssl/            # Base Hardening + SSL + Headers
│   │   ├── conf/
│   │   ├── Dockerfile
│   │   ├── README.md
│   │   └── ssl/
│   ├── task_2_waf/                 # ModSecurity (WAF)
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── task_3_owasp/               # Reglas OWASP CRS
│   │   ├── Dockerfile
│   │   └── README.md
│   ├── task_4_dos/                 # Protección Anti-DoS (ModEvasive)
│   │   ├── Dockerfile
│   │   ├── evasive.conf
│   │   └── README.md
│   ├── task_5_hardening/           # Best Practices (Timeout, Methods, Cookies)
│   │   ├── Dockerfile
│   │   ├── hardening-extra.conf
│   │   └── README.md
│   └── task_6_nginx/               # Implementación equivalente en Nginx
│       ├── conf/
│       ├── Dockerfile
│       ├── README.md
│       └── ssl/

```

---

## 🚀 Índice de Despliegue (Tasks)

### [Task 1: Base Hardening + SSL](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_1_base_ssl)

**Objetivo:** Establecer la imagen base segura. Incluye generación de certificados SSL autofirmados, ocultación de la versión del servidor (`ServerTokens Prod`) y aplicación de cabeceras de seguridad estrictas (HSTS, CSP, X-XSS-Protection).

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr1](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr1)

**Validación:**
El servidor fuerza HTTPS, oculta la versión de Apache y entrega cabeceras de seguridad.

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr1:latest
# Run: docker run -d -p 8080:80 -p 8443:443 brean19/pps-pr1:latest

```

---

### [Task 2: Web Application Firewall (WAF)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_2_waf)

**Objetivo:** Implementación de seguridad activa mediante **ModSecurity**. Configuración en modo "Bloqueo" (SecRuleEngine On) para interceptar tráfico malicioso. Hereda de Task 1.

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr2](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr2)

**Validación:**
Bloqueo efectivo de ataques XSS básicos (`<script>alert(1)</script>`) devolviendo error 403.

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr2:latest
# Run: docker run -d -p 8081:80 -p 8444:443 brean19/pps-pr2:latest

```

---

### [Task 3: OWASP Core Rule Set](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_3_owasp)

**Objetivo:** Integración del conjunto de reglas **OWASP CRS** para mitigar el Top 10 de vulnerabilidades web (SQL Injection, Path Traversal, etc.). Hereda de Task 2.

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr3](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr3)

**Validación:**
Detección y bloqueo de intentos de Command Injection (`/bin/bash`) y Path Traversal (`../../etc/passwd`).

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr3:latest
# Run: docker run -d -p 8082:80 -p 8445:443 brean19/pps-pr3:latest

```

---

### [Task 4: Protección Anti-DoS](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_4_dos)

**Objetivo:** Mitigación de ataques de Denegación de Servicio y Fuerza Bruta mediante **mod_evasive**. Configuración de umbrales agresivos para detección rápida y baneo temporal de IPs. Hereda de Task 3.

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr4](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr4)

**Validación:**
Prueba de estrés con `Apache Bench`. El servidor bloquea el 94% de las peticiones masivas.

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr4:latest
# Run: docker run -d -p 8083:80 -p 8446:443 brean19/pps-pr4:latest

```

---

### [Task 5: Advanced Hardening (Best Practices)](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_5_hardening)

**Objetivo:** Ajuste fino basado en guías CIS/Geekflare. Reducción de Timeouts (Slowloris), deshabilitación de métodos HTTP peligrosos (TRACE/OPTIONS) y aseguramiento de Cookies. Hereda de Task 4.

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr5](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr5)

**Validación:**
Rechazo explícito (403 Forbidden) de métodos no permitidos como OPTIONS.

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr5:latest
# Run: docker run -d -p 8085:80 -p 8448:443 brean19/pps-pr5:latest

```

---

### [Task 6: Nginx Secure Server](https://github.com/brean-rb/RA3_PPS_10813818/tree/main/RA3/RA3_1/task_6_nginx)

**Objetivo:** Implementación "Standalone" en **Nginx**. Replica todas las medidas de seguridad: SSL/TLS, HSTS, CSP, X-Frame-Options y ocultación de versión (`server_tokens off`).

* **Estado:** ✅ Completado
* **DockerHub:** [brean19/pps-pr6](https://www.google.com/search?q=https://hub.docker.com/r/brean19/pps-pr6)

**Validación:**
Nginx sirve contenido seguro validando todas las cabeceras de seguridad inyectadas manualmente.

**Despliegue Rápido:**

```bash
docker pull brean19/pps-pr6:latest
# Run: docker run -d -p 8084:80 -p 8447:443 brean19/pps-pr6:latest

```

---

## ⚠️ Nota Técnica sobre RA3_1

Para la realización del RA3_1, se ha optado por una **Estrategia de Construcción en Cascada (Layered Docker Builds)**. 

Se ha modificado el orden lógico sugerido en el enunciado para garantizar la coherencia técnica:
1. **Prioridad SSL:** Se ha integrado la Práctica 3.2 (Certificados) en la **Fase 1**.
2. **Justificación:** La implementación de **HSTS** (requerida en el hardening básico) exige una conexión HTTPS funcional. Sin certificados previos, no es posible aplicar políticas de transporte estricto.

Todas las imágenes Docker generadas son públicas y accesibles en DockerHub bajo el usuario: `brean19`.

**Autor:** brean-rb / 10813818
**Licencia:** Academic / MIT

