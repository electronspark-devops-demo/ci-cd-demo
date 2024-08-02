FROM nginx:alpine

# Copy your custom nginx.conf to the container
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

# Copy your application files to the Nginx html directory
COPY html /usr/share/nginx/html

# Use envsubst to substitute environment variables in nginx.conf and config.js
RUN apk add --no-cache gettext
CMD ["/bin/sh", "-c", "envsubst '\$FRONTEND_DOMAIN \$BACKEND_DOMAIN' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf && envsubst '\$BACKEND_DOMAIN' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js && exec nginx -g 'daemon off;'"]
