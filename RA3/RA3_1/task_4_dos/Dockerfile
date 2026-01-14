# 1. HERENCIA: Usamos la imagen con OWASP (Fase 3)
FROM pps/pr3

# 2. Instalamos mod_evasive
# Fuente: Hardening del servidor.pdf (menciona mod_evasive)
RUN apt-get update && apt-get install -y \
    libapache2-mod-evasive \
    && apt-get clean

# 3. Creamos el directorio de logs y ajustamos permisos
# Es vital que www-data (el usuario de Apache) pueda escribir aquí
RUN mkdir -p /var/log/mod_evasive && \
    chown -R www-data:www-data /var/log/mod_evasive

# 4. Copiamos nuestra configuración agresiva
COPY evasive.conf /etc/apache2/mods-available/evasive.conf

# 5. Ejecutamos Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
