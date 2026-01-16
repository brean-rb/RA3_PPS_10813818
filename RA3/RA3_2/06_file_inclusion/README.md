Aquí tienes el **`README.md`** para la práctica de **File Inclusion**, perfectamente encapsulado en un único bloque de código.

He puesto las instrucciones paso a paso con la URL exacta que hay que copiar, usando el marcador `<IP_DEL_SERVIDOR>` para que sirva siempre, cambie o no la IP.

Copia todo lo que hay dentro del recuadro:

```markdown
# Práctica 06: File Inclusion

## 📝 Descripción
La vulnerabilidad de **Inclusión de Archivos (File Inclusion)** permite a un atacante leer archivos internos del servidor que no deberían ser accesibles públicamente. Esto ocurre cuando la aplicación web carga un archivo basándose en una entrada de usuario (un parámetro en la URL) sin validarla correctamente.

En esta práctica, explotaremos esta vulnerabilidad para leer el archivo `/etc/passwd`, que contiene la lista de usuarios del sistema Linux del servidor.

---

## 🟢 Nivel: LOW

En el nivel bajo, la aplicación coge el nombre del archivo directamente del parámetro `page` de la URL y lo abre. No hay ningún tipo de filtro.

**Pasos para reproducirlo:**
1.  Entra en la sección **File Inclusion**.
2.  Observa que la URL termina en `?page=include.php`.
3.  Vamos a cambiar ese archivo por la ruta absoluta del archivo de contraseñas de Linux.

**URL del Ataque:**
Copia esta dirección en tu navegador (sustituyendo la IP):
```text
http://<IP_DEL_SERVIDOR>:9090/vulnerabilities/fi/?page=/etc/passwd

```

**Evidencia:**
Al cargar la página, en lugar de la web normal, veremos el contenido del archivo de usuarios del sistema (`root:x:0:0...`), confirmando que tenemos acceso de lectura al sistema de archivos del servidor.
![File Inclusion Low](../asset/06_fi_low.png)

---

## 🟠 Nivel: MEDIUM

En el nivel medio, el servidor intenta protegerse bloqueando ciertos patrones como `../` (para evitar subir directorios) o `http://` (para evitar incluir archivos remotos). Sin embargo, a menudo olvida bloquear las **rutas absolutas** directas.

**Pasos para reproducirlo:**

1. Cambia el nivel de seguridad a **Medium**.
2. Volvemos a probar exactamente el mismo ataque que en el nivel bajo, ya que al pedir el archivo directamente desde la raíz (`/etc/passwd`), el filtro no detecta nada malicioso.

**URL del Ataque:**
Copia esta dirección en tu navegador:

```text
http://<IP_DEL_SERVIDOR>:9090/vulnerabilities/fi/?page=/etc/passwd

```

**Evidencia:**
El filtro falla y la aplicación vuelve a mostrarnos el contenido del archivo `/etc/passwd`, demostrando que la seguridad implementada es insuficiente.

![File Inclusion Medium](../asset/06_fi_medium.png)

