FROM nginx:alpine

# Copy your custom nginx.conf to the container
COPY nginx.conf /etc/nginx/nginx.conf

# Copy your application files to the Nginx html directory
COPY html /usr/share/nginx/html

# Use envsubst to substitute environment variables in config.template.js
RUN apk add --no-cache gettext
CMD ["/bin/sh", "-c", "envsubst < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js && exec nginx -g 'daemon off;'"]
