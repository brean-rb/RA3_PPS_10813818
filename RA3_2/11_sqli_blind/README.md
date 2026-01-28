# Práctica 11: SQL Injection (Blind)

## 📝 Descripción
En la inyección SQL "Ciega" (Blind SQLi), la base de datos no devuelve los datos solicitados directamente en la página web (no veremos listas de contraseñas). En su lugar, la aplicación solo responde con un mensaje genérico de "Verdadero" o "Falso" (o tarda en responder), dependiendo de si nuestra consulta fue exitosa.

Como atacantes, debemos actuar como en el juego "Adivina quién", haciendo preguntas de Sí/No a la base de datos para reconstruir la información poco a poco.

---

## 🟢 Nivel: LOW

En el nivel bajo, inyectaremos una condición lógica (`AND 1=1`) para verificar si podemos manipular la consulta. Si la web responde que el usuario existe, confirmamos que tenemos control sobre la sentencia SQL.

**Payload:**
Le decimos a la base de datos: "Búscame el ID 1 **Y** confírmame que 1 es igual a 1".
```sql
1' AND 1=1#

```

**Pasos para reproducirlo:**

1. Introduce el payload anterior en el cuadro de texto "User ID".
2. Pulsa **Submit**.

**Evidencia:**
La aplicación devuelve el mensaje **"User ID exists in the database"**. Si hubiéramos puesto `1=0` (falso), diría "User ID is MISSING", demostrando que la respuesta de la web depende de nuestra lógica inyectada.

![Blind SQLi Low](../asset/11_sqli_blind_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, el campo es un menú desplegable y se filtran las comillas. Al igual que en la inyección SQL normal, usaremos el método de intercepción para enviar una inyección numérica (sin comillas).

**⚠️ Nota Importante:**
Usaremos **Firefox** y la función **"Edit and Resend"** para modificar el valor que envía el formulario, ya que no podemos escribir en el desplegable.

**Payload:**
Inyectamos la misma lógica pero sin comillas, ya que el campo `id` es un número.

```sql
1 AND 1=1#

```

**Pasos detallados:**

1. Selecciona un usuario cualquiera en el desplegable y pulsa **Submit**.
2. Abre las herramientas de desarrollador (**F12**) y ve a la pestaña **Network**.
3. Busca la petición `POST` realizada, haz **Clic Derecho -> Edit and Resend**.
4. En el cuerpo de la petición (Body), modifica el parámetro `id` con nuestro payload:
```text
id=1 AND 1=1#&Submit=Submit

```


5. Pulsa **Send**.
6. Ve a la pestaña **Response** para ver el resultado en el código HTML.

**Evidencia:**
En la respuesta del servidor, encontramos la frase **"User ID exists in the database"**, confirmando que hemos logrado inyectar código SQL a pesar de los filtros y el menú desplegable.

![Blind SQLi Medium](../asset/11_sqli_blind_medium.png)

