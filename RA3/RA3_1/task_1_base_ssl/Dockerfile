# Imagen base ligera
FROM debian:bookworm-slim

# Instalación de paquetes necesarios
RUN apt-get update && apt-get install -y \
    apache2 \
    openssl \
    curl \
    && apt-get clean

# Habilitar módulos de Apache (SSL, Headers, Rewrite)
RUN a2enmod ssl headers rewrite

# Crear directorios y copiar archivos locales al contenedor
RUN mkdir -p /etc/apache2/ssl
COPY ssl/apache.key /etc/apache2/ssl/
COPY ssl/apache.crt /etc/apache2/ssl/
COPY conf/user-hardening.conf /etc/apache2/conf-available/user-hardening.conf
COPY conf/default-ssl.conf /etc/apache2/sites-available/default-ssl.conf

# Activar configuraciones y sitio seguro
RUN a2enconf user-hardening && \
    a2ensite default-ssl

# Exponer puertos HTTP y HTTPS
EXPOSE 80 443

# Ejecutar Apache en primer plano
CMD ["apache2ctl", "-D", "FOREGROUND"]

