FROM postgres:14.1
LABEL authors="humanlearning"

WORKDIR /usr/src/app

COPY create_dw_table.sql create_dw_table.sql

RUN apt-get update -y

USER postgres

RUN pg_createcluster 14 main &&\
    service postgresql start &&\
    psql -d postgres -f create_dw_table.sql

USER root

EXPOSE 5432