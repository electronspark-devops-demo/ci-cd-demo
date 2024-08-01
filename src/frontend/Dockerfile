FROM nginx:alpine
COPY ./html /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
RUN apk add --no-cache gettext
CMD [   "/bin/sh", \
        "-c", \
        "envsubst < /usr/share/nginx/html/config.template.js > /usr/share/nginx/html/config.js && exec nginx -g 'daemon off;'"]
