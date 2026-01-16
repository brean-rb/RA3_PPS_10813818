# Práctica 03: Content Security Policy (CSP) Bypass

## 📝 Descripción
La **Content Security Policy (CSP)** es una capa de seguridad que ayuda a detectar y mitigar ciertos tipos de ataques, como el Cross-Site Scripting (XSS) y la inyección de datos. Funciona definiendo qué fuentes de contenido dinámico son permitidas.

En esta práctica, explotamos configuraciones débiles en la CSP de DVWA para ejecutar código JavaScript no autorizado.

---

## 🟢 Nivel: LOW

En este nivel, la política de seguridad define una "lista blanca" de dominios de confianza desde los cuales se pueden cargar scripts. Analizando las cabeceras o el comportamiento, se descubre que **pastebin.com** está permitido.

**Metodología:**
1.  Se identifica que la CSP permite la carga de scripts externos desde `https://pastebin.com`.
2.  Se utiliza un enlace a un recurso alojado en dicha plataforma (`https://pastebin.com/dl/Lnamji4V`) para inyectarlo en la aplicación.

**Evidencia:**
Como se muestra en la captura, el navegador permite la carga del recurso externo (visible en la pestaña *Sources* y *Network*), validando que la CSP ha sido eludida al permitir un dominio de terceros.
*(Nota: En la consola se observa un error de sintaxis derivado del contenido del script remoto, pero la carga del archivo, que es la vulnerabilidad de CSP, se ha completado con éxito).*

![CSP Bypass Low](../asset/03_csp_low.png.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, la CSP implementa el uso de un **nonce** (un número de un solo uso) y la cabecera `X-XSS-Protection`. La teoría dicta que cada script debe tener un atributo `nonce` que coincida con el generado por el servidor.

**Vulnerabilidad:**
La implementación es defectuosa porque el valor del `nonce` es **estático** (no cambia entre peticiones) o es predecible. Esto permite a un atacante reutilizar el valor legítimo para firmar sus propios scripts maliciosos.

**Payload utilizado:**
```html
<script nonce="TmV2ZXIgZ29pbmcgdG8gZ2l2ZSB5b3UgdXA=">alert(document.cookie)</script>ç
```
**Evidencia:** 
Al incluir el script con el nonce correcto, la protección CSP valida el código como "confiable" y ejecuta la alerta mostrando las cookies de sesión.
![CSP Bypass Low](../asset/03_csp_medium.png.png)
