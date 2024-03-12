FROM postgres:14.1
LABEL authors="humanlearning"

WORKDIR /usr/src/app

COPY create_dw_table.sql create_dw_table.sql

RUN apt-get update -y

USER postgres

RUN pg_createcluster 14 main &&\
    service postgresql start &&\
    psql -d postgres -f create_dw_table.sql &&\
    sed -i 's|local   all             postgres                                peer|local\tall\t\tpostgres\t\t\t\ttrust|' /etc/postgresql/14/main/pg_hba.conf &&\
    echo 'host\tall\t\tall\t\t0.0.0.0/0\t\ttrust' >> /etc/postgresql/14/main/pg_hba.conf

USER root

EXPOSE 5432
