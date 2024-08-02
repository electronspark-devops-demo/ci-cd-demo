FROM nginx:alpine

# Copy your custom nginx.conf to the container
COPY nginx.conf.template /etc/nginx/templates/nginx.conf.template

# Copy your application files to the Nginx html directory
COPY html /usr/share/nginx/html

COPY launch.sh /root/launch.sh

# Use envsubst to substitute environment variables in nginx.conf and config.js
RUN apk add --no-cache gettext
CMD ["/bin/sh", "-c", "sh /root/launch.sh"]
