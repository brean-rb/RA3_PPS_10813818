# Task 2: Web Application Firewall (ModSecurity)

En esta fase implementamos una capa de seguridad activa mediante **ModSecurity**, un WAF (Web Application Firewall) que inspecciona el tráfico HTTP en tiempo real para bloquear ataques maliciosos antes de que lleguen a la aplicación.

Esta imagen **hereda** directamente de la `Task 1`, por lo que mantiene toda la configuración SSL y Hardening base.

## 🎯 Objetivos de Seguridad

1.  **Inspección de Tráfico:** Analizar las peticiones entrantes en busca de patrones maliciosos.
2.  **Bloqueo Activo:** Configuración del motor de reglas en modo `On` para rechazar peticiones sospechosas.
3.  **Protección Base:** Mitigación de ataques comunes como XSS (Cross-Site Scripting) básicos.

## 📂 Estructura de Archivos

* `Dockerfile`: Script de construcción que instala el módulo WAF sobre la imagen base.

## 🛠️ Procedimiento de Construcción

### 1. Herencia y Dockerfile
Se utiliza la estrategia de **Layered Builds** (capas). No reinstalamos Apache, sino que extendemos la imagen anterior:

```dockerfile
FROM pps/pr1
RUN apt-get update && apt-get install -y libapache2-mod-security2

```

### 2. Configuración del WAF

Por defecto, ModSecurity viene en modo "Detección" (solo avisa). Para que proteja realmente, se modifica la directiva `SecRuleEngine` a `On` en el archivo `/etc/modsecurity/modsecurity.conf`:

```bash
sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' ...

```

### 3. Docker Build & Run

Comandos utilizados para generar la imagen:

```bash
# Construir imagen (Etiqueta pr2)
docker build -t pps/pr2 .

# Ejecutar contenedor (Puertos 8081->80, 8444->443 para no chocar con Task 1)
docker run -d -p 8081:80 -p 8444:443 --name apache_waf pps/pr2

```

## ✅ Validación

Se simula un ataque de **Cross-Site Scripting (XSS)** inyectando un script en la URL. El WAF detecta el patrón `<script>` y bloquea la conexión.

**Comando de ataque:**

```bash
curl -I -k "https://localhost:8444/?q=<script>alert(1)</script>"

```

**Resultado esperado:** `HTTP/1.1 403 Forbidden` .

**Evidencia:**
![Validación WAF](../asset/02_validacion_waf.png)

## ☁️ DockerHub

La imagen está disponible públicamente:

```bash
docker pull brean19/pps-pr2:latest

```
