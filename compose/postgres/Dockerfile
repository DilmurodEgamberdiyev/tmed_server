FROM postgres:16.2-alpine

RUN apk add --no-cache postgresql-pg_cron && \
    cp /usr/lib/postgresql16/pg_cron.so /usr/local/lib/postgresql/ && \
    cp /usr/share/postgresql16/extension/* /usr/local/share/postgresql/extension

COPY compose/postgres/postgresql.conf /var/lib/postgresql/data/

CMD ["postgres"]
