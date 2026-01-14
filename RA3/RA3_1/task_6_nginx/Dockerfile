# Usamos la imagen oficial ligera de Nginx
FROM nginx:latest

# Instalamos curl por si necesitamos debug
RUN apt-get update && apt-get install -y curl && apt-get clean

# Copiamos los certificados generados
RUN mkdir -p /etc/nginx/ssl
COPY ssl/nginx.key /etc/nginx/ssl/
COPY ssl/nginx.crt /etc/nginx/ssl/

# Copiamos nuestra configuración de seguridad
# Sobrescribimos la 'default.conf' que trae Nginx
COPY conf/default.conf /etc/nginx/conf.d/default.conf

# Exponemos puertos web
EXPOSE 80 443

# Nginx se ejecuta solo, no hace falta CMD
