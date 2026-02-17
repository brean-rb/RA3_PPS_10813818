# Práctica 10: SQL Injection (SQLi)

**Autor:** Ruben Ferrer (brean-rb / 10813818)
**Asignatura:** Puesta en Producción Segura

## Descripción de la Vulnerabilidad
La **Inyección SQL (SQLi)** es una vulnerabilidad de seguridad web que permite a un atacante interferir con las consultas que una aplicación realiza a su base de datos. Esto ocurre generalmente cuando la aplicación inserta datos proporcionados por el usuario directamente en una cadena de consulta SQL sin la debida sanitización o parametrización.

El impacto de esta vulnerabilidad es crítico, ya que puede permitir a un atacante visualizar datos no autorizados (como contraseñas o datos personales), modificar o eliminar información, e incluso, en ciertos escenarios, tomar el control administrativo del servidor de base de datos.



---

## Nivel: LOW

### Análisis
En el nivel de seguridad bajo, la aplicación solicita un identificador de usuario (User ID) a través de un cuadro de texto. El código backend toma esta entrada y la concatena directamente en la consulta SQL.

**Consulta Vulnerable (Conceptual):**
```sql
SELECT first_name, last_name FROM users WHERE user_id = '$id';

```

### Metodología de Explotación

Para explotar este fallo, utilizamos el operador `UNION`. Este operador permite combinar los resultados de la consulta original con los resultados de una nueva consulta inyectada por el atacante.

**Payload:**

```sql
1' UNION SELECT user, password FROM users#

```

* `1'`: Cierra la cadena de texto original de la consulta.
* `UNION SELECT ...`: Añade la consulta maliciosa para extraer usuarios y contraseñas.
* `#`: Comenta el resto de la consulta original para evitar errores de sintaxis SQL.

### Reproducción

1. Introducir el payload anterior en el campo "User ID".
2. Pulsar **Submit**.

### Evidencia

La aplicación ejecuta la consulta modificada y devuelve una lista combinada que incluye el ID solicitado y el volcado completo de la tabla `users` (nombres de usuario y hashes de contraseñas).

![SQL Injection Low](../asset/10_sqli_low.png)

---

## Nivel: MEDIUM

### Análisis

En el nivel medio, la aplicación implementa dos medidas de seguridad:

1. **Restricción de Interfaz:** Utiliza un menú desplegable (`<select>`) para forzar al usuario a elegir un ID predefinido.
2. **Sanitización:** Aplica la función `mysql_real_escape_string()` a la entrada, la cual escapa caracteres especiales como las comillas simples (`'`).

**Vulnerabilidad:**
La consulta SQL en este nivel trata el parámetro `id` como un número entero, no como una cadena. Por lo tanto, la consulta no utiliza comillas alrededor de la variable `$id`.

```sql
SELECT first_name, last_name FROM users WHERE user_id = $id;

```

Al no requerir comillas para cerrar la consulta, la función `mysql_real_escape_string` (diseñada para escapar comillas) resulta ineficaz. La vulnerabilidad persiste a través de una inyección numérica directa.

### Metodología: Intercepción de Peticiones

Dado que el menú desplegable impide la escritura libre, es necesario interceptar y modificar la petición HTTP POST enviada al servidor.

1. **Preparación:** Seleccionar cualquier usuario válido y pulsar **Submit**.
2. **Intercepción:** Abrir las herramientas de desarrollador (F12), ir a la pestaña **Network** y localizar la petición POST.
3. **Edición:** Utilizar la función **Edit and Resend** (Firefox) para modificar el cuerpo de la petición.
4. **Payload:** Sustituir el valor del parámetro `id` por la inyección SQL (sin comillas):
```text
id=1 UNION SELECT user, password FROM users#&Submit=Submit

```


5. **Envío:** Ejecutar la petición modificada.

### Evidencia

Al inspeccionar la respuesta del servidor (Pestaña Response), se observa que la inyección numérica ha sido procesada exitosamente, devolviendo nuevamente las credenciales de los usuarios.

![SQL Injection Medium](../asset/10_sqli_medium.png)
