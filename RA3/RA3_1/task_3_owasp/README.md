# Task 3: OWASP Core Rule Set (CRS)

En esta fase se eleva significativamente el perfil de seguridad del servidor web mediante la integración del **OWASP Core Rule Set (CRS)**. Mientras que la tarea anterior activó el motor WAF, esta fase le proporciona la "inteligencia" necesaria: un conjunto de reglas mantenidas por la comunidad para detectar y bloquear ataques complejos.

Esta imagen sigue la estrategia de **Layered Builds**, heredando de la `Task 2` (WAF activado), sumando las reglas a la configuración existente.

## 📂 Estructura del Directorio

Esta tarea no requiere archivos de configuración locales complejos, ya que las reglas se descargan dinámicamente durante la construcción para asegurar la última versión.

```text
task_3_owasp/
├── Dockerfile                  # Script de automatización (Git clone + Configuración)
└── README.md                   # Documentación técnica
```

---

## 🛠️ Configuración Técnica

### 1. Estrategia de Obtención de Reglas (Dockerfile)
En lugar de "quemar" (copiar) archivos estáticos locales que pueden quedar obsoletos, el `Dockerfile` está programado para clonar el repositorio oficial de SpiderLabs/OWASP durante la construcción.

### 2. Configuración en Apache
El proceso automatizado realiza las siguientes acciones críticas:
1.  **Clonado:** Descarga el set de reglas en `/usr/share/modsecurity-crs`.
2.  **Setup:** Renombra el archivo de configuración de ejemplo (`crs-setup.conf.example`) a producción.
3.  **Inclusión:** Modifica la configuración de Apache para cargar primero el setup y luego todas las reglas (`*.conf`).

**Snippet del Dockerfile:**
```dockerfile
# Heredar del WAF activo
FROM pps/pr2

# Instalar Git
RUN apt-get update && apt-get install -y git && apt-get clean

# Descargar reglas oficiales (OWASP CRS)
RUN rm -rf /usr/share/modsecurity-crs && \
    git clone https://github.com/coreruleset/coreruleset.git /usr/share/modsecurity-crs

# Preparar archivo de configuración
RUN mv /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf

# Vincular reglas a Apache (security2.conf)
RUN echo "IncludeOptional /usr/share/modsecurity-crs/crs-setup.conf" >> /etc/apache2/mods-enabled/security2.conf && \
    echo "IncludeOptional /usr/share/modsecurity-crs/rules/*.conf" >> /etc/apache2/mods-enabled/security2.conf

CMD ["apache2ctl", "-D", "FOREGROUND"]
```

---

## 🚀 Despliegue y Validación

### Construcción Manual
```bash
# Construir la imagen
docker build -t pps/pr3 .

# Ejecutar contenedor (Puertos 8082/8445)
docker run -d -p 8082:80 -p 8445:443 --name apache_owasp pps/pr3
```

### Validación de Seguridad (Pruebas de Penetración)
Se ejecutan dos vectores de ataque comunes para verificar que las reglas específicas del CRS están operativas.

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
Ambos comandos deben devolver estrictamente **403 Forbidden**. Esto confirma que el CRS ha identificado los patrones de ataque y ha ordenado al motor WAF bloquear la conexión.

![Validación OWASP](../asset/03_validacion_owasp.png)

---

## ☁️ DockerHub

Imagen pre-construida disponible para despliegue rápido:

```bash
docker pull brean19/pps-pr3:latest
```
