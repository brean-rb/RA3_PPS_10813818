# Task 4: Anti-DoS Protection (ModEvasive)

En esta fase se añade una capa de defensa contra ataques de **Denegación de Servicio (DoS)** y fuerza bruta. Se utiliza el módulo `mod_evasive`, el cual mantiene una tabla interna de direcciones IP y URI para detectar patrones de acceso anómalos. Si una IP supera los umbrales definidos, es bloqueada temporalmente (lista negra), devolviendo un error 403.

Esta imagen sigue la estrategia de **Layered Builds**, heredando de la `Task 3` (OWASP + WAF), sumando la protección volumétrica a la seguridad aplicativa.

## 📂 Estructura del Directorio

Se introduce un archivo de configuración personalizado para definir los umbrales de sensibilidad del módulo:

```text
task_4_dos/
├── evasive.conf                # Configuración de umbrales (Agresiva para pruebas)
├── Dockerfile                  # Instalación del módulo y gestión de logs
└── README.md                   # Documentación técnica
```

---

## 🛠️ Configuración Técnica

### 1. Configuración de Umbrales (`evasive.conf`)
Para efectos de esta práctica, se han configurado umbrales **extremadamente bajos (agresivos)**. Esto garantiza que el sistema de protección salte inmediatamente durante las pruebas de estrés, facilitando la validación.

```apache
<IfModule mod_evasive20.c>
    DOSHashTableSize    3097
    DOSPageCount        2       # Bloquea si pide la misma página 2 veces en 1 seg
    DOSSiteCount        10      # Bloquea si hace 10 peticiones totales al sitio en 1 seg
    DOSPageInterval     1
    DOSSiteInterval     1
    DOSBlockingPeriod   10      # La IP queda baneada por 10 segundos
    DOSLogDir           "/var/log/mod_evasive"
</IfModule>
```

### 2. Gestión de Logs y Permisos (Dockerfile)
Un punto crítico para que `mod_evasive` funcione es que el usuario de Apache (`www-data`) tenga permisos de escritura en el directorio de logs. Si esto falla, el módulo no bloquea.

**Snippet del Dockerfile:**
```dockerfile
# Heredar de la imagen anterior (OWASP)
FROM pps/pr3

# Instalar módulo
RUN apt-get update && apt-get install -y libapache2-mod-evasive && apt-get clean

# Crear directorio de logs y asignar propiedad al usuario web
RUN mkdir -p /var/log/mod_evasive && \
    chown -R www-data:www-data /var/log/mod_evasive

# Inyectar configuración
COPY evasive.conf /etc/apache2/mods-available/evasive.conf

CMD ["apache2ctl", "-D", "FOREGROUND"]
```

---

## 🚀 Despliegue y Validación

### Construcción Manual
```bash
# Construir la imagen
docker build -t pps/pr4 .

# Ejecutar contenedor (Puertos 8083/8446)
docker run -d -p 8083:80 -p 8446:443 --name apache_dos pps/pr4
```

### Validación de Estrés (Stress Test)
Utilizamos **Apache Bench (ab)** para simular un ataque de denegación de servicio, lanzando 100 peticiones con una concurrencia de 10 usuarios simultáneos.

**Comando de ataque:**
```bash
# -n 100: Número total de peticiones
# -c 10:  Concurrencia (usuarios simultáneos)
ab -n 100 -c 10 http://localhost:8083/
```

**Resultado Esperado:**
El reporte final debe mostrar un alto número de **"Failed requests"** o **"Non-2xx responses"**. Esto indica que, tras las primeras peticiones aceptadas, el servidor detectó el ataque y comenzó a rechazar el resto con errores `403 Forbidden`.

**Evidencia:**
![Validación DoS](../asset/04_validacion_dos.png)

---

## ☁️ DockerHub

Imagen pre-construida disponible para despliegue rápido:

```bash
docker pull brean19/pps-pr4:latest
```
