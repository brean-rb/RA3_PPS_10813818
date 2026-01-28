# Task 5: Apache Best Practices Hardening

En esta fase final dedicada a Apache, aplicamos medidas de "ajuste fino" (*fine-tuning*) recomendadas por guías de seguridad reconocidas (CIS, Geekflare). El objetivo es reducir la superficie de ataque mitigando vulnerabilidades lentas, deshabilitando funcionalidades innecesarias y asegurando los permisos del sistema de archivos.

Esta imagen sigue la estrategia de **Layered Builds**, heredando de la `Task 4` (Anti-DoS), consolidando así todas las capas de seguridad previas.

## 📂 Estructura del Directorio

Se introduce un archivo de configuración específico para directivas de endurecimiento y se modifican permisos en el Dockerfile:

```text
task_5_hardening/
├── hardening-extra.conf        # Directivas: Timeout, Métodos HTTP, Cookies
├── Dockerfile                  # Aplicación de permisos (Principio de Mínimo Privilegio)
└── README.md                   # Documentación técnica
```

---

## 🛠️ Configuración Técnica

### 1. Directivas de Endurecimiento (`hardening-extra.conf`)
Se aplican configuraciones críticas para mitigar ataques de agotamiento de recursos y reconocimiento:

```apache
# 1. Mitigación Slow Loris:
# Reducimos el tiempo de espera para liberar conexiones lentas maliciosas.
Timeout 60

# 2. Bloqueo de Protocolos Obsoletos:
# Rechazamos peticiones HTTP/1.0 (inseguras frente a secuestro de sesión).
RewriteCond %{THE_REQUEST} !HTTP/1.1$
RewriteRule .* - [F]

# 3. Seguridad de Sesión:
# Forzamos flags HttpOnly y Secure en todas las cookies.
<IfModule mod_headers.c>
    Header edit Set-Cookie ^(.*)$ $1;HttpOnly;Secure
</IfModule>

# 4. Reducción de Superficie de Ataque:
# Bloqueamos métodos peligrosos (TRACE, TRACK, OPTIONS). Solo permitimos lo esencial.
<Location />
    <LimitExcept GET POST HEAD>
        Deny from all
    </LimitExcept>
</Location>
```

### 2. Permisos del Sistema de Archivos (Dockerfile)
Siguiendo el **Principio de Mínimo Privilegio**, se restringen los permisos sobre los binarios y configuraciones del servidor para que solo el usuario root y el grupo de Apache (`www-data`) tengan acceso.

**Snippet del Dockerfile:**
```dockerfile
# Heredar de la imagen Anti-DoS
FROM pps/pr4

# Inyectar configuración extra
COPY hardening-extra.conf /etc/apache2/conf-available/hardening-extra.conf
RUN a2enconf hardening-extra

# HARDENING DE PERMISOS (chmod 750)
# Se elimina el acceso de lectura/ejecución para 'otros' usuarios en carpetas críticas.
RUN chmod -R 750 /etc/apache2/conf-available && \
    chmod -R 750 /usr/sbin/apache2

CMD ["apache2ctl", "-D", "FOREGROUND"]
```

---

## 🚀 Despliegue y Validación

### Construcción Manual
```bash
# Construir la imagen
docker build -t pps/pr5 .

# Ejecutar contenedor (Puertos 8085/8448)
docker run -d -p 8085:80 -p 8448:443 --name apache_best_practices pps/pr5
```

### Validación de Métodos HTTP
Verificamos que el servidor rechaza activamente métodos que suelen utilizarse para reconocimiento o depuración (como `OPTIONS`).

**Comando de prueba:**
```bash
# Intentamos usar el método OPTIONS
curl -I -k -X OPTIONS https://localhost:8448
```

**Resultado Esperado:**
El servidor debe responder con un código **403 Forbidden** (o 405 Method Not Allowed), confirmando que la directiva `<LimitExcept>` está funcionando y protegiendo el servidor de métodos no autorizados.

**Evidencia:**
![Validación Hardening](../asset/05_validacion_hardening.png)

---

## ☁️ DockerHub

Imagen pre-construida disponible para despliegue rápido:

```bash
docker pull brean19/pps-pr5:latest
```
