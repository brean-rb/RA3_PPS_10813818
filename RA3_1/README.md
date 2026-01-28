# RA3.1 - Apache & Nginx Hardening Project

> [!NOTE]
> **Nota Técnica sobre la Estrategia de Construcción**
>
> Para la realización del RA3_1, se ha optado por una **Estrategia de Construcción en Cascada (Layered Docker Builds)**.
>
> Se ha modificado el orden lógico sugerido en el enunciado original para garantizar la coherencia técnica, integrando la **Práctica 3.2 (Certificados SSL)** directamente en la **Fase 1**.
>
> **Justificación:** La implementación de políticas de seguridad estrictas como **HSTS** (HTTP Strict Transport Security) exige una conexión HTTPS funcional como pre-requisito. Sin certificados SSL configurados desde el inicio, no es posible aplicar un hardening efectivo en las capas posteriores.

## Descripción del Proyecto

Este documento consolida la implementación técnica de las prácticas **3.1 (Hardening)**, **3.2 (Certificados)** y **3.3 (Best Practices)**.

## Repositorio de Imágenes Docker
Todas las imágenes utilizadas en este proyecto están publicadas y son accesibles públicamente en mi perfil de DockerHub:

**[Acceder al Perfil de DockerHub (brean19)](https://hub.docker.com/u/brean19)**

El objetivo es asegurar progresivamente servidores web Apache y Nginx mediante la contenerización en Docker. Cada "Task" o tarea representa una capa de seguridad adicional que hereda de la anterior, creando una arquitectura de defensa en profundidad.

## Estructura del Repositorio

El proyecto se organiza en directorios modulares correspondientes a cada fase de seguridad:

```text
RA3_1/
├── asset/                      # Evidencias y capturas de validación
├── README.md                   # Documentación Principal (Este archivo)
├── task_1_base_ssl/            # Fase 1: Base Hardening + SSL + Headers
├── task_2_waf/                 # Fase 2: ModSecurity (WAF)
├── task_3_owasp/               # Fase 3: Reglas OWASP CRS
├── task_4_dos/                 # Fase 4: Protección Anti-DoS (ModEvasive)
├── task_5_hardening/           # Fase 5: Best Practices (Timeouts, Methods)
└── task_6_nginx/               # Fase 6: Implementación equivalente en Nginx

```

---

## Guía de Despliegue por Fases

A continuación se detallan las instrucciones para desplegar y validar cada capa de seguridad. Las imágenes están alojadas públicamente en DockerHub.

### Task 1: Base Hardening + SSL

**Ubicación:** [Ver Documentación Técnica (Task 1)](./task_1_base_ssl/README.md)

Establece la imagen base segura. Incluye la generación de certificados SSL autofirmados, la ocultación de la versión del servidor (`ServerTokens Prod`) y la aplicación de cabeceras de seguridad estrictas (HSTS, CSP, X-XSS-Protection).

* **Imagen Docker:** `brean19/pps-pr1`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr1:latest
docker run -d -p 8080:80 -p 8443:443 --name pps-task1 brean19/pps-pr1:latest

```

**Validación:**
Acceder a `https://localhost:8443`. Verificar que el servidor fuerza la redirección HTTPS y oculta la firma de versión en las cabeceras de respuesta.

---

### Task 2: Web Application Firewall (WAF)

**Ubicación:** [Ver Documentación Técnica (Task 2)](./task_2_waf/README.md)

Implementación de seguridad activa mediante **ModSecurity**. Se configura en modo "DetectionOnly" o "On" (Bloqueo) para interceptar e inspeccionar el tráfico HTTP malicioso. Esta capa hereda la configuración de la Task 1.

* **Imagen Docker:** `brean19/pps-pr2`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr2:latest
docker run -d -p 8081:80 -p 8444:443 --name pps-task2 brean19/pps-pr2:latest

```

**Validación:**
Intentar un ataque XSS básico (`<script>alert(1)</script>`) en la URL o argumentos. El servidor debe devolver un error 403 Forbidden.

---

### Task 3: OWASP Core Rule Set

**Ubicación:** [Ver Documentación Técnica (Task 3)](./task_3_owasp/README.md)

Integración del conjunto de reglas estándar **OWASP CRS** sobre ModSecurity. Mitiga automáticamente las vulnerabilidades del OWASP Top 10 (SQL Injection, Path Traversal, etc.) sin necesidad de escribir reglas manuales.

* **Imagen Docker:** `brean19/pps-pr3`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr3:latest
docker run -d -p 8082:80 -p 8445:443 --name pps-task3 brean19/pps-pr3:latest

```

**Validación:**
Simular un ataque de acceso a archivos del sistema (`../../etc/passwd`). La petición debe ser bloqueada por las reglas de OWASP.

---

### Task 4: Protección Anti-DoS

**Ubicación:** [Ver Documentación Técnica (Task 4)](./task_4_dos/README.md)

Mitigación de ataques de Denegación de Servicio (DoS) y Fuerza Bruta mediante el módulo **mod_evasive**. Se establecen umbrales de petición agresivos para detectar y banear temporalmente IPs sospechosas.

* **Imagen Docker:** `brean19/pps-pr4`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr4:latest
docker run -d -p 8083:80 -p 8446:443 --name pps-task4 brean19/pps-pr4:latest

```

**Validación:**
Utilizar herramientas de estrés como `ab` (Apache Bench) o scripts en Python. El servidor debe comenzar a rechazar conexiones (Retorno 403) tras superar el umbral configurado.

---

### Task 5: Advanced Hardening (Best Practices)

**Ubicación:** [Ver Documentación Técnica (Task 5)](./task_5_hardening/README.md)

Ajuste fino de la configuración basado en guías CIS y Geekflare. Incluye la reducción de Timeouts para evitar ataques Slowloris, la deshabilitación estricta de métodos HTTP innecesarios (TRACE, OPTIONS, TRACK) y el aseguramiento de cookies (Flags Secure y HttpOnly).

* **Imagen Docker:** `brean19/pps-pr5`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr5:latest
docker run -d -p 8085:80 -p 8448:443 --name pps-task5 brean19/pps-pr5:latest

```

**Validación:**
Enviar una petición con el método `OPTIONS`. El servidor debe responder con un código de error indicando que el método no está permitido.

---

### Task 6: Nginx Secure Server

**Ubicación:** [Ver Documentación Técnica (Task 6)](./task_6_nginx/README.md)

Implementación independiente utilizando **Nginx**. Replica todas las medidas de seguridad aplicadas anteriormente en Apache: SSL/TLS, HSTS, CSP, X-Frame-Options y ocultación de versión (`server_tokens off`).

* **Imagen Docker:** `brean19/pps-pr6`

**Comando de Despliegue:**

```bash
docker pull brean19/pps-pr6:latest
docker run -d -p 8084:80 -p 8447:443 --name pps-task6 brean19/pps-pr6:latest

```

**Validación:**
Inspeccionar las cabeceras de respuesta del servidor Nginx para verificar la presencia de las directivas de seguridad y la ausencia de la versión del servidor.

---

**Autor:** Ruben Ferrer 
**Asignatura:** Puesta en Producción Segura


