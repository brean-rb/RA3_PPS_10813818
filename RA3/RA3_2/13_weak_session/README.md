# Práctica 13: Weak Session IDs

## 📝 Descripción
La gestión de sesiones es crítica para la seguridad web. Cuando un usuario se autentica, el servidor le asigna un "Identificador de Sesión" (Session ID) temporal, que suele guardarse en una cookie.

[cite_start]Si estos identificadores se generan de forma predecible (secuencial, basado en la hora, etc.), un atacante puede adivinar el ID de un usuario legítimo (como el administrador) y secuestrar su sesión sin necesitar su contraseña[cite: 407, 409].

---

## 🟢 Nivel: LOW

En el nivel bajo, la generación del ID de sesión es extremadamente insegura. El sistema utiliza un contador simple que se incrementa en 1 cada vez que se solicita una nueva sesión.

**Análisis:**
[cite_start]Al observar la cookie llamada `dvwaSession`, vemos valores como `1`, `2`, `3`... Esto permite a un atacante deducir fácilmente cualquier sesión activa probando números secuenciales[cite: 407].

**Pasos para reproducirlo:**
1.  Ve al apartado **Weak Session IDs**.
2.  Pulsa el botón **Generate Session ID**.
3.  Abre las herramientas de desarrollador (**F12**) y ve a la pestaña **Storage** (o Application) > **Cookies**.
4.  Localiza la cookie `dvwaSession` y observa su valor numérico simple.

**Evidencia:**
Captura mostrando la cookie `dvwaSession` con un valor secuencial bajo (ej: 5, 6, etc.), demostrando la predictibilidad del sistema.

![Weak Session Low](../asset/13_weak_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, el desarrollador ha intentado mejorar la seguridad dejando de usar números simples. Sin embargo, el método elegido sigue siendo predecible: utiliza la marca de tiempo actual (Unix Timestamp).

**Análisis:**
El valor de la cookie `dvwaSession` ahora es un número largo (ej: `1737108923`). Este número corresponde a los segundos transcurridos desde el 1 de enero de 1970 (época Unix). [cite_start]Un atacante solo necesita saber la hora aproximada en la que el usuario se conectó para realizar un ataque de fuerza bruta sobre un rango de tiempo reducido[cite: 409].

**Pasos para reproducirlo:**
1.  Cambia la seguridad a **Medium**.
2.  Pulsa el botón **Generate Session ID**.
3.  Inspecciona nuevamente la cookie `dvwaSession` en las herramientas de desarrollador.
4.  Comprueba que el valor coincide con el *timestamp* actual (puedes verificarlo en un conversor online).

**Evidencia:**
Captura mostrando la cookie con un valor numérico largo correspondiente a la fecha y hora actual.

![Weak Session Medium](../asset/13_weak_medium.png)
