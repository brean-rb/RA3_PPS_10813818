# Práctica 12: Stored Cross Site Scripting (XSS)

## 📝 Descripción
El **Cross-Site Scripting Almacenado (Stored XSS)** es una de las vulnerabilidades más críticas en aplicaciones web. Ocurre cuando la aplicación guarda la entrada del usuario (como un comentario o un mensaje) en su base de datos sin sanearla correctamente.

A diferencia del XSS Reflejado, aquí el ataque es **persistente**: cualquier usuario (incluido el administrador) que visite la página infectada ejecutará el código malicioso automáticamente, simplemente por cargar la web.

---

## 🟢 Nivel: LOW

En el nivel bajo, la aplicación posee un libro de visitas (Guestbook) con campos para Nombre y Mensaje. El campo de "Mensaje" no realiza ninguna limpieza, permitiendo guardar scripts completos.

**Payload:**
Utilizamos la etiqueta de imagen con error para ejecutar JavaScript, igual que en la práctica anterior.
```html
<img src=x onerror="alert(document.cookie)">

```

**Pasos para reproducirlo:**

1. Ve al apartado **XSS (Stored)**.
2. Escribe cualquier nombre en el campo "Name".
3. En el campo "Message", pega el payload anterior.
4. Pulsa **Sign Guestbook**.

**Evidencia:**
Al guardarse el mensaje, la página se recarga para mostrarlo y el script se ejecuta inmediatamente, mostrando el pop-up con las cookies. Si recargas la página, el pop-up volverá a salir porque el ataque está grabado en la base de datos.

![Stored XSS Low](../asset/12_xss_stored_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, el desarrollador ha protegido el campo "Message" usando la función `htmlspecialchars` (que neutraliza las etiquetas HTML). Sin embargo, el campo "Name" sigue siendo vulnerable, aunque tiene dos protecciones:

1. Un filtro que busca la palabra `<script>`.
2. Un límite de longitud en el HTML (`maxlength="10"`) que impide escribir textos largos.

**Metodología:**
Para saltar estas protecciones:

1. Escribimos el script mezclando mayúsculas y minúsculas (`<sCrIpT>`) para evadir el filtro de texto.
2. Modificamos el código HTML de la página en nuestro navegador para ampliar el límite de caracteres.

**Payload:**

```html
<sCrIpT>alert(document.cookie)</ScRiPt>

```

**Pasos detallados:**

1. Cambia la seguridad a **Medium**.
2. Haz **Clic Derecho** sobre la caja de texto **Name** y elige **Inspect** (Inspeccionar).
3. En el código HTML que aparece, busca el atributo `maxlength="10"`.
4. Haz doble clic sobre el número "10", cámbialo por **100** y pulsa Enter.
5. Ahora que cabe el texto, pega el payload de arriba en el campo **Name**.
6. Escribe cualquier cosa en el mensaje y pulsa **Sign Guestbook**.



**Evidencia:**
El nombre se guarda en la base de datos interpretándose como código. Al mostrarse en la lista, el navegador ejecuta el script y muestra las cookies.

![Stored XSS Medium](../asset/12_xss_stored_medium.png)

