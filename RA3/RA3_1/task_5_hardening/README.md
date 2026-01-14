# Task 5: Apache Best Practices Hardening

En esta fase final de Apache, aplicamos una serie de configuraciones de "ajuste fino" (Hardening) recomendadas por guías de seguridad como Geekflare y la documentación oficial de Apache.

Esta imagen **hereda** de la `Task 4` (Anti-DoS).

## 🎯 Objetivos de Seguridad

1.  **Mitigación Slow Loris:** Reducción del `Timeout` para evitar conexiones lentas que agoten los recursos.
2.  **Reducción de Superficie de Ataque:** Desactivación de métodos HTTP innecesarios y peligrosos (como TRACE o TRACK).
3.  **Seguridad de Sesión:** Forzado de cookies con flags `HttpOnly` y `Secure`.
4.  **Protección de Archivos:** Restricción de permisos en binarios y configuración (chmod 750).

## 📂 Estructura de Archivos

* `Dockerfile`: Aplica los permisos de sistema de archivos (chmod).
* `hardening-extra.conf`: Contiene las directivas de configuración de Apache.

## 🛠️ Procedimiento de Construcción

### 1. Configuración Extra (hardening-extra.conf)
Se añaden directivas críticas que no vienen por defecto:

```apache
Timeout 60                                          # Mitigación DoS lento
RewriteCond %{THE_REQUEST} !HTTP/1.1$               # Bloquear HTTP 1.0
Header edit Set-Cookie ^(.*)$ $1;HttpOnly;Secure    # Proteger Cookies

# Bloquear todo método que no sea GET, POST o HEAD
<Location />
    <LimitExcept GET POST HEAD>
        Deny from all
    </LimitExcept>
</Location>

```

### 2. Permisos en Dockerfile

Siguiendo el principio de mínimo privilegio, se retiran permisos de lectura/ejecución a "otros" usuarios en carpetas sensibles:

```dockerfile
# Permisos 750 (Solo root y grupo www-data)
RUN chmod -R 750 /etc/apache2/conf-available && \
    chmod -R 750 /usr/sbin/apache2

```

### 3. Docker Build & Run

Comandos utilizados para generar la imagen:

```bash
# Construir imagen (Etiqueta pr5)
docker build -t pps/pr5 .

# Ejecutar contenedor (Puertos 8085->80, 8448->443)
docker run -d -p 8085:80 -p 8448:443 --name apache_best_practices pps/pr5

```

## ✅ Validación

Se verifica que el servidor rechace métodos HTTP no permitidos. Intentamos realizar una petición con el método `OPTIONS` (comúnmente usado para reconocimiento).

**Comando:**

```bash
curl -I -k -X OPTIONS https://localhost:8448

```

**Resultado esperado:**
El servidor debe bloquear la petición devolviendo un código `HTTP/1.1 403 Forbidden`.

**Evidencia:**

![Validación Hardening](../asset/05_validacion_hardening.png)

## ☁️ DockerHub

La imagen está disponible públicamente:

```bash
docker pull brean19/pps-pr5:latest

```
