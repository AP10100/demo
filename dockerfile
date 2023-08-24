# for configure of apache2 server
# FROM ubuntu/apache2:latest
# COPY index /var//www/html
# COPY apache.conf /etc/apache2/ports.conf
# EXPOSE 8090

# for configure of apache tomcat server
FROM tomcat:latest
# USER root
COPY index /usr/local/tomcat/webapps/index

