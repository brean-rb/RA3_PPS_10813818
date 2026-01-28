# 1. HERENCIA: Usamos la imagen con WAF de la Fase 2
FROM pps/pr2

# 2. Instalamos Git para clonar las reglas oficiales
RUN apt-get update && apt-get install -y git && apt-get clean

# 3. Descargamos las reglas OWASP Core Rule Set (CRS)
# Fuente: Hardening del servidor.pdf (git clone)
RUN rm -rf /usr/share/modsecurity-crs && \
    git clone https://github.com/coreruleset/coreruleset.git /usr/share/modsecurity-crs

# 4. Configuramos el archivo de setup del CRS
RUN mv /usr/share/modsecurity-crs/crs-setup.conf.example /usr/share/modsecurity-crs/crs-setup.conf

# 5. Vinculamos las reglas a Apache
# Editamos security2.conf para incluir las reglas descargadas
# Fuente: Hardening del servidor.pdf (IncludeOptional ...)
RUN echo "IncludeOptional /usr/share/modsecurity-crs/crs-setup.conf" >> /etc/apache2/mods-enabled/security2.conf && \
    echo "IncludeOptional /usr/share/modsecurity-crs/rules/*.conf" >> /etc/apache2/mods-enabled/security2.conf

# 6. Ejecutamos Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]

