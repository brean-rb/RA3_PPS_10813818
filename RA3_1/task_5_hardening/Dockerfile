# 1. HERENCIA: Usamos la imagen de la Fase 4 (Anti-DoS)
FROM pps/pr4

# 2. Copiamos la configuración extra
COPY hardening-extra.conf /etc/apache2/conf-available/hardening-extra.conf

# 3. Activamos la configuración
RUN a2enconf hardening-extra

# 4. PROTECCIÓN DE BINARIOS Y CONFIGURACIÓN (Permisos 750)
# [cite_start]Fuente: Apache Web Server Hardening Guide [cite: 462]
# Quitamos permisos a 'otros' en carpetas críticas
RUN chmod -R 750 /etc/apache2/conf-available && \
    chmod -R 750 /usr/sbin/apache2

# 5. Ejecutamos Apache
CMD ["apache2ctl", "-D", "FOREGROUND"]
