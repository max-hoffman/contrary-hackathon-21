FROM nginx:alpine

# remove any existing config files
RUN rm etc/nginx/conf.d/*

# copy config files
COPY default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
