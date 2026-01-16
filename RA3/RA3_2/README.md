# RA3.2 - Hacking Web con DVWA

Este proyecto documenta la resolución de desafíos de seguridad web utilizando **Damn Vulnerable Web Application (DVWA)**. El objetivo es identificar y explotar vulnerabilidades en un entorno controlado para comprender los riesgos de seguridad en aplicaciones PHP/MySQL.

## 🎯 Objetivos

Realizar pruebas de penetración (*pentesting*) abordando las vulnerabilidades del **OWASP Top 10** en los niveles de dificultad **Low** y **Medium**.

## 🏗️ Arquitectura del Laboratorio

Para la realización de estas prácticas se ha configurado un entorno de red Cliente-Servidor:

* **Víctima (Servidor):** Máquina Virtual **Ubuntu Server** (CLI).
    * Ejecuta el servicio vulnerable mediante **Docker**.
    * IP: `<IP_UBUNTU>` (Puerto 9090).
* **Atacante (Cliente):** Máquina Física/Virtual **Kali Linux** (GUI).
    * Se utiliza para navegar por la web, interceptar tráfico y lanzar ataques.

---

## 🛠️ Despliegue e Instalación

Sigue estos pasos estrictamente en la máquina **Ubuntu Server** para levantar el entorno vulnerable.

### Paso 1: Descargar la imagen
Descargamos la imagen oficial desde Docker Hub para asegurarnos de tener la última versión disponible localmente.

```bash
sudo docker pull vulnerables/web-dvwa
```

### Paso 2: Desplegar el contenedor
Lanzamos el contenedor exponiéndolo en el puerto **9090** del host. Usamos este puerto para evitar conflictos con otros servicios web (como Apache o Nginx) que puedan estar corriendo en el puerto 80 estándar.

```bash
sudo docker run -d -p 9090:80 --name dvwa vulnerables/web-dvwa
```

### Paso 3: Verificación
Comprobamos que el contenedor está funcionando correctamente. En la columna `STATUS` debe aparecer como 'Up'.

```bash
sudo docker ps
```

---

## ⚙️ Configuración Inicial (Desde Kali Linux)

Una vez desplegado el contenedor, la configuración se realiza vía web desde el navegador de la máquina atacante (**Kali Linux**):

1.  **Acceso:** Abre Firefox y ve a `http://<IP-UBUNTU>:9090`.
2.  **Login:** Introduce las credenciales por defecto.
    * **Usuario:** `admin`
    * **Contraseña:** `password`
3.  **Inicialización de Base de Datos:**
    * Al acceder, el sistema detectará que la base de datos no existe.
    * Haz clic en el botón **"Create / Reset Database"** situado al final de la página.
    * Espera a la redirección al login.
4.  **Ajuste de Nivel:**
    * Una vez dentro, ve al menú izquierdo **"DVWA Security"**.
    * Ajusta el nivel de seguridad a **Low** y pulsa **Submit**.

---

## 📂 Índice de Actividades

Documentación detallada y evidencias de explotación para cada vulnerabilidad:

1.  [Brute Force](./01_brute_force/README.md)
2.  [Command Injection](./02_command_injection/README.md)
3.  [CSP Bypass](./03_csp_bypass/README.md)
4.  [CSRF](./04_csrf/README.md)
5.  [DOM Based XSS](./05_dom_xss/README.md)
6.  [File Inclusion](./06_file_inclusion/README.md)
7.  [File Upload](./07_file_upload/README.md)
8.  [JavaScript Attacks](./08_javascript/README.md)
9.  [Reflected XSS](./09_reflected_xss/README.md)
10. [SQL Injection](./10_sqli/README.md)
11. [SQL Injection (Blind)](./11_sqli_blind/README.md)
12. [Stored XSS](./12_stored_xss/README.md)
13. [Weak Session IDs](./13_weak_ids/README.md)

---
**Autor:** Ruben Ferrer Marquez
