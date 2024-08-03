#!/bin/sh

envsubst '\$FRONTEND_DOMAIN \$BACKEND_DOMAIN' < /etc/nginx/templates/nginx.conf.template > /etc/nginx/nginx.conf
envsubst '\$BACKEND_DOMAIN' < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js
# exec nginx -g 'daemon off;'

EXPOSE 5000
CMD ["python", "app.py"]