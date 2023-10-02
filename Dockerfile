# for configure of apache2 server
# FROM ubuntu/apache2:latest
# COPY index /var//www/html
# COPY apache.conf /etc/apache2/ports.conf
# EXPOSE 8090

# for configure of apache tomcat server
FROM tomcat:latest
# USER root
COPY index /usr/local/tomcat/webapps/index
# By default apche tomcat image is running on 8080 port so if we want to run it locally by docker run then map 
# ....the docker run command like :::  docker run -it -d -p 9500:8080 <image_name>....localhost:9500
