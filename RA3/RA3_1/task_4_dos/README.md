# Task 4: Anti-DoS (ModEvasive)

En esta fase añadimos una capa de protección contra ataques de **Denegación de Servicio (DoS)** y fuerza bruta. Utilizamos el módulo `mod_evasive`, que rastrea las direcciones IP entrantes y las bloquea temporalmente si superan ciertos umbrales de frecuencia.

Esta imagen **hereda** de la `Task 3` (OWASP + WAF).

## 🎯 Objetivos de Seguridad

1.  **Disponibilidad del Servicio:** Evitar que el servidor se sature por un exceso de peticiones de un solo cliente.
2.  **Protección contra Fuerza Bruta:** Bloquear IPs que intenten adivinar contraseñas o rutas rápidamente.
3.  **Baneo Automático:** Configuración de listas negras temporales (10 segundos) para IPs agresivas.

## 📂 Estructura de Archivos

* `Dockerfile`: Instalación del módulo y gestión de permisos de logs.
* `evasive.conf`: Configuración personalizada con umbrales muy bajos (agresivos) para facilitar la validación.

## 🛠️ Procedimiento de Construcción

### 1. Configuración Agresiva (evasive.conf)
Para efectos de la práctica, se han configurado umbrales mínimos para garantizar que el sistema de protección salte inmediatamente durante las pruebas:

```apache
DOSHashTableSize    3097
DOSPageCount        2       # Bloquea si pide la misma página 2 veces en 1 seg
DOSSiteCount        10      # Bloquea si hace 10 peticiones totales en 1 seg
DOSBlockingPeriod   10      # Tiempo de castigo (segundos)

```

### 2. Dockerfile

Se instala el módulo y se asegura que el usuario de Apache (`www-data`) tenga permisos de escritura en el directorio de logs, paso crítico para que `mod_evasive` funcione:

```dockerfile
# Instalación
RUN apt-get install -y libapache2-mod-evasive

# Permisos de Log
RUN mkdir -p /var/log/mod_evasive && \
    chown -R www-data:www-data /var/log/mod_evasive

```

### 3. Docker Build & Run

Comandos utilizados para generar la imagen:

```bash
# Construir imagen (Etiqueta pr4)
docker build -t pps/pr4 .

# Ejecutar contenedor (Puertos 8083->80, 8446->443)
docker run -d -p 8083:80 -p 8446:443 --name apache_dos pps/pr4

```

## ✅ Validación

Se utiliza la herramienta **Apache Bench (ab)** para realizar una prueba de estrés (Stress Test) simulando 10 usuarios concurrentes lanzando 100 peticiones a alta velocidad.

**Comando de ataque:**

```bash
ab -n 100 -c 10 http://localhost:8083/

```

**Resultado esperado:**
El reporte debe mostrar un alto número de **"Failed requests"** o **"Non-2xx responses"**, indicando que el servidor ha empezado a responder con errores `403 Forbidden` tras detectar el ataque.

**Evidencia:**

## ☁️ DockerHub

![Validación DoS](../asset/04_validacion_dos.png)

La imagen está disponible públicamente:

```bash
docker pull brean19/pps-pr4:latest

```

