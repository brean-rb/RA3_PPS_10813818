# Práctica 05: DOM Based Cross Site Scripting (XSS)

## 📝 Descripción
El **Cross-Site Scripting basado en DOM (DOM XSS)** es una vulnerabilidad que ocurre en el lado del cliente (navegador). Sucede cuando la aplicación web procesa datos de una fuente no confiable (como la URL) de manera insegura dentro del Modelo de Objetos del Documento (DOM), ejecutando código JavaScript malicioso.

A diferencia del XSS Reflejado o Almacenado, en el DOM XSS la respuesta del servidor no necesita contener el script malicioso; es el propio script legítimo de la página el que lo ejecuta al leer la entrada del usuario.

---

## 🟢 Nivel: LOW

En el nivel bajo, la aplicación utiliza un script que lee el parámetro `default` de la URL y lo imprime directamente en el documento HTML para seleccionar el idioma por defecto, sin realizar ninguna limpieza o codificación.

**Payload:**
```text
<script>alert(document.cookie)</script>

```

**Resultado:**
Al modificar el parámetro en la URL, el navegador interpreta las etiquetas de script inyectadas y ejecuta el código JavaScript, mostrando las cookies de sesión.

**Evidencia:**
![DOM XSS Low](../asset/05_xss_dom_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, la aplicación intenta filtrar la entrada buscando la etiqueta `<script>` para bloquearla. Además, el contexto de inyección cambia: el texto se inserta dentro de una etiqueta `<select>`, específicamente dentro de un `<option>`.

**Metodología:**
Para eludir este filtro, utilizamos una técnica de "escape" de etiquetas.

1. Cerramos forzosamente las etiquetas `<option>` y `<select>` existentes.
2. Utilizamos un vector de ataque alternativo que no requiera la palabra prohibida `script`, como una etiqueta de imagen (`<img>`) con un evento de error (`onerror`).

**Payload:**

```text
></option></select><img src=x onerror="alert(document.cookie)">

```

**Resultado:**
El navegador cierra el selector de idioma y procesa la imagen inválida. Al fallar la carga de la imagen (`src=x`), se dispara el evento `onerror`, ejecutando nuestro código JavaScript.

**Evidencia:**
![DOM XSS Medium](../asset/05_xss_dom_medium.png)
