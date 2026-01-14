# 1. HERENCIA: Usamos TU imagen de la Fase 1 como base
FROM pps/pr1

# 2. Instalamos ModSecurity (El WAF)
# Fuente: Hardening del servidor.pdf (libapache2-mod-security2)
RUN apt-get update && apt-get install -y \
    libapache2-mod-security2 \
    && apt-get clean

# 3. Activamos el módulo y la configuración recomendada por defecto
# Fuente: Hardening del servidor.pdf (cp modsecurity.conf-recommended)
RUN cp /etc/modsecurity/modsecurity.conf-recommended /etc/modsecurity/modsecurity.conf && \
    sed -i 's/SecRuleEngine DetectionOnly/SecRuleEngine On/' /etc/modsecurity/modsecurity.conf

# 4. (Opcional) Limpieza de logs antiguos al arrancar
CMD ["apache2ctl", "-D", "FOREGROUND"]
