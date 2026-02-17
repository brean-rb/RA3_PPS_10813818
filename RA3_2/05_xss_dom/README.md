# Práctica 05: DOM Based Cross Site Scripting (XSS)

**Autor:** Ruben Ferrer (brean-rb / 10813818)
**Asignatura:** Puesta en Producción Segura

## Descripción de la Vulnerabilidad
El **Cross-Site Scripting basado en DOM (DOM XSS)** es una vulnerabilidad que ocurre en el lado del cliente (navegador). Sucede cuando una aplicación contiene JavaScript que procesa datos de una fuente no confiable (como la URL) de manera insegura, escribiendo esos datos directamente en el Modelo de Objetos del Documento (DOM) sin la debida sanitización[cite: 16].

A diferencia del XSS Reflejado o Almacenado, en el DOM XSS la carga útil maliciosa se ejecuta como resultado de la modificación del entorno del DOM en el navegador de la víctima, a menudo sin que los datos lleguen siquiera al servidor backend.

---

## Nivel: LOW

### Análisis
En el nivel de seguridad bajo, la aplicación utiliza un script para generar un menú desplegable de selección de idioma. El código JavaScript lee el valor del parámetro `default` de la URL y lo escribe directamente en el documento HTML utilizando `document.write()` o similar, sin ningún tipo de filtro.

### Reproducción
1.  Identificar el parámetro vulnerable en la URL: `default`.
2.  Sustituir el valor legítimo (`English`) por un script malicioso estándar.

**Payload:**
```text
http://<IP_DEL_SERVIDOR>:9090/vulnerabilities/xss_d/?default=<script>alert(document.cookie)</script>

```

### Evidencia

Al cargar la URL, el navegador procesa el parámetro, encuentra las etiquetas `<script>` y las ejecuta inmediatamente, mostrando las cookies de sesión.

![DOM XSS Low](../asset/05_xss_dom_low.png)

---

## Nivel: MEDIUM

### Análisis

En el nivel medio, la aplicación implementa un filtro básico que busca y elimina la cadena `<script>` en el parámetro de entrada. Además, el contexto de inyección ha cambiado: el texto inyectado se coloca dentro de una etiqueta `<select>`, específicamente dentro de una etiqueta `<option>`.

**Desafíos:**

1. **Contexto HTML:** El código inyectado queda "atrapado" dentro del menú desplegable, donde los scripts no se ejecutan.
2. **Filtro:** No se pueden utilizar etiquetas `<script>` directas.

### Metodología de Explotación

Para ejecutar código, es necesario "escapar" del contexto actual cerrando las etiquetas HTML contenedoras y utilizar un vector alternativo que no requiera la etiqueta script, como los manejadores de eventos en imágenes.

1. **Romper el contexto:** Se inyecta `></option></select>` para cerrar el menú desplegable y volver al cuerpo del documento.
2. **Vector de ataque:** Se utiliza una etiqueta de imagen (`<img>`) con una fuente inválida (`src=x`) para forzar un error de carga.
3. **Ejecución:** Se aprovecha el manejador de eventos `onerror` para ejecutar el código JavaScript cuando la carga de la imagen falla.

**Payload:**

```text
http://<IP_DEL_SERVIDOR>:9090/vulnerabilities/xss_d/?default=></option></select><img src=x onerror="alert(document.cookie)">

```

### Evidencia

El navegador interpreta el cierre de etiquetas, intenta renderizar la imagen, falla al buscar el recurso "x" y dispara el evento `onerror`, ejecutando la alerta con las cookies.

![DOM XSS Medium](../asset/05_xss_dom_medium.png)
