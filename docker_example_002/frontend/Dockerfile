FROM nginx:1.31.1

RUN rm -rf /usr/share/nginx/html/*

COPY . /usr/share/nginx/html

EXPOSE 80

# Start Nginx in the foreground (required for Docker containers)
CMD ["nginx", "-g", "daemon off;"]