# Práctica 07: File Upload

## 📝 Descripción
La vulnerabilidad de **Subida de Archivos (File Upload)** ocurre cuando un servidor web permite a los usuarios subir archivos sin validar correctamente su nombre, tamaño, tipo o contenido.

Un atacante puede aprovechar esto para subir archivos maliciosos (como scripts PHP) que, al ser ejecutados por el servidor, permiten tomar el control del mismo, leer archivos sensibles o establecer una conexión remota (Reverse Shell).

---

## 🟢 Nivel: LOW

En el nivel bajo, la aplicación no realiza ninguna validación sobre el archivo subido. Confía ciegamente en el usuario, permitiendo subir cualquier extensión, incluyendo `.php`.

**Pasos para reproducirlo:**
1.  Creamos un archivo llamado `malicioso.php` con el siguiente contenido:
    `<?php echo "<h1>¡HACKEADO!</h1>"; phpinfo(); ?>`
2.  Vamos a la sección **File Upload** y subimos el archivo.
3.  La web nos confirmará la ruta de subida (`../../hackable/uploads/malicioso.php`).

**URL del Ataque:**
Para ver el resultado y ejecutar el código, visita esta dirección:
```text
http://<IP_DEL_SERVIDOR>:9090/hackable/uploads/malicioso.php

```

**Evidencia:**
Al visitar la URL, el servidor ejecuta nuestro código PHP, mostrando el mensaje "HACKEADO" y la configuración interna de PHP.
![File Upload Low](../asset/07_upload_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, el servidor verifica el **MIME Type** (tipo de contenido) del archivo. Si detecta que es un script (`application/x-php`), rechaza la subida. Solo permite imágenes (`image/jpeg` o `image/png`).

**⚠️ Nota Importante:**
Para este nivel se recomienda encarecidamente usar el navegador **Mozilla Firefox**. Su herramienta de desarrollador tiene una función llamada **"Edit and Resend"** que facilita enormemente la manipulación de peticiones, algo que en Chrome es mucho más complejo de realizar.

**Metodología (Bypass de Content-Type):**
Engañaremos al servidor interceptando la petición y cambiando la etiqueta del tipo de archivo, aunque el contenido siga siendo PHP malicioso.

1. Intentamos subir `malicioso.php` y observamos que falla.
2. Abrimos las herramientas de desarrollador (**F12**) y vamos a la pestaña **Network**.
3. Localizamos la petición `POST` fallida, hacemos **Clic Derecho -> Edit and Resend**.
4. Buscamos la línea `Content-Type: application/x-php` y la cambiamos por:
`Content-Type: image/png`
5. Pulsamos **Send**.

**URL del Ataque:**
El archivo se habrá subido correctamente. Accedemos a la misma ruta que antes:

```text
http://<IP_DEL_SERVIDOR>:9090/hackable/uploads/malicioso.php

```

**Evidencia:**
A pesar del filtro, el servidor ha aceptado el archivo PHP creyendo que era una imagen, permitiéndonos ejecutar el código nuevamente.
![File Upload Medium](../asset/07_upload_medium.png)
