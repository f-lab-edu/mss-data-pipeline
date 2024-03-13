FROM postgres:16
LABEL authors="humanlearning"

ENV POSTGRES_PASSWORD="1234" \
    POSTGRES_USER="postgres" \
    POSTGRES_DB="postgres"


WORKDIR /usr/src/app

#COPY create_dw_table.sql create_dw_table.sql
COPY create_dw_table.sql /docker-entrypoint-initdb.d

RUN apt-get update -y && \
    apt-get install vim sudo procps -y

USER postgres

RUN pg_createcluster 16 main &&\
#    /etc/init.d/postgresql start &&\
#    psql -U postgres -d postgres -f create_dw_table.sql &&\
    sed -i 's|local   all             all                                     peer|local\tall\t\tall\t\t\t\t\ttrust|' /etc/postgresql/16/main/pg_hba.conf &&\
    echo 'host\tall\t\tall\t\t0.0.0.0/0\t\ttrust' >> /etc/postgresql/16/main/pg_hba.conf

USER root

EXPOSE 5432

#ENTRYPOINT ["psql", "-d", "postgres", "-f", "create_dw_table.sql"]
