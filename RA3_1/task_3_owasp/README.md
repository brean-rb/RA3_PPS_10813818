# Task 3: OWASP Core Rule Set (CRS)

En esta fase se eleva significativamente el perfil de seguridad del servidor web mediante la integración del **OWASP Core Rule Set (CRS)**. Mientras que la tarea anterior activó el motor WAF (ModSecurity), esta fase le proporciona la inteligencia necesaria mediante un conjunto de reglas mantenidas por la comunidad para detectar y bloquear ataques complejos.

Esta imagen sigue la estrategia de **Layered Builds** (Construcción por Capas), heredando de la `Task 2` (WAF activado) y añadiendo las reglas a la configuración existente sin alterar la base.

## Estructura del Directorio

Esta tarea no requiere archivos de configuración locales complejos, ya que las reglas se descargan dinámicamente durante la construcción para asegurar la utilización de la versión más reciente.

```text
task_3_owasp/
├── Dockerfile                  # Script de automatización (Git clone + Configuración)
└── README.md                   # Documentación técnica

```

---

## Configuración Técnica

### 1. Estrategia de Obtención de Reglas (Dockerfile)

En lugar de copiar archivos estáticos locales que pueden quedar obsoletos rápidamente, el `Dockerfile` está programado para clonar el repositorio oficial de SpiderLabs/OWASP directamente durante la fase de construcción.

### 2. Configuración en Apache

El proceso automatizado realiza las siguientes acciones críticas dentro del contenedor:

1. **Clonado:** Descarga el set de reglas en el directorio `/usr/share/modsecurity-crs`.
2. **Setup:** Renombra el archivo de configuración de ejemplo (`crs-setup.conf.example`) a producción (`crs-setup.conf`).
3. **Inclusión:** Modifica la configuración del módulo de Apache (`security2.conf`) para cargar primero el archivo de setup y posteriormente todas las reglas (`*.conf`).

**Extracto del Dockerfile:**

```dockerfile
# Heredar del WAF activo (Task 2)
FROM pps/pr2

# Instalar Git para descargar las reglas
RUN apt-get update && apt-get install -y git && apt-get clean

# Descargar reglas oficiales (OWASP CRS) desde GitHub
RUN rm -rf /usr/share/modsecurity-crs && \
    git clone [https://github.com/coreruleset/coreruleset.git](https://github.com/coreruleset/coreruleset.git) /usr/share/modsecurity-crs

# Preparar archivo de configuración inicial
RUN mv /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf

# Vincular las reglas a la configuración de Apache (security2.conf)
# Se incluyen el setup y todas las reglas .conf descargadas
RUN echo "IncludeOptional /usr/share/modsecurity-crs/crs-setup.conf" >> /etc/apache2/mods-enabled/security2.conf && \
    echo "IncludeOptional /usr/share/modsecurity-crs/rules/*.conf" >> /etc/apache2/mods-enabled/security2.conf

CMD ["apache2ctl", "-D", "FOREGROUND"]

```

---

## Despliegue y Validación

### Construcción Manual

```bash
# Construir la imagen localmente
docker build -t pps/pr3 .

# Ejecutar contenedor
# Nota: Se utilizan los puertos 8082/8445 para evitar conflictos con tareas anteriores
docker run -d -p 8082:80 -p 8445:443 --name apache_owasp pps/pr3

```

### Validación de Seguridad (Pruebas de Penetración)

Se ejecutan dos vectores de ataque comunes para verificar que las reglas específicas del CRS están operativas y bloqueando tráfico.

**1. Prueba de Command Injection (RCE)**
Intento de invocar una shell de comandos a través de un parámetro URL.

```bash
curl -I -k "https://localhost:8445/?exec=/bin/bash"

```

**2. Prueba de Path Traversal (LFI)**
Intento de acceder a archivos sensibles del sistema saliendo del directorio raíz web.

```bash
curl -I -k "https://localhost:8445/?file=../../etc/passwd"

```

**Resultado Esperado:**
Ambos comandos deben devolver un código de estado **403 Forbidden**. Esto confirma que el CRS ha identificado los patrones de ataque (acceso a `/bin/bash` y recorrido de directorios `../`) y ha ordenado al motor WAF bloquear la conexión.

**Evidencia de validación:**
![Validación OWASP](../asset/03_validacion_owasp.png)

---

## Imagen Docker (DockerHub)

Imagen pre-construida disponible para despliegue rápido:

```bash
docker pull brean19/pps-pr3:latest

```

---

**Autor:** Ruben Ferrer 
