FROM nginx:stable-alpine

COPY ./client/dist/ /usr/share/nginx/html

COPY ./docker/nginx.conf /etc/nginx/nginx.conf
