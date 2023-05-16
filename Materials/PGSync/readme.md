Готовый пример со всеми нужными изменениями находится в этой папке, запуск через `docker compose up --build`

Во flask представлены 2 метода: 

Поиск владельца по именованию экипировки, за которую он отвечает:

```shell
curl --location --request GET 'http://127.0.0.1:12862/holders/search_by_equipment?title=Мяч'
```

Поиск экипировки по названию через n-gram индекс:
```shell
curl --location --request GET 'http://127.0.0.1:12862/autocomplete?word=па'
```

1. В `docker-compose.yml` добавить

```yaml
  elasticsearch:
    container_name: ${APP_NAME}-elasticsearch
    image: bitnami/elasticsearch:8.5.0
    ports:
      - "${ELASTIC_PORT}:9200"
    environment:
      - xpack.security.enabled=false
      - network.host=127.0.0.1
      - http.host=0.0.0.0
    healthcheck:
      test: curl -u elastic:elastic -s -f elasticsearch:9200/_cat/health >/dev/null || exit 1
      interval: 1s
      retries: 100
  pgsync:
    container_name: ${APP_NAME}-pgsync
    build:
      context: ./pgsync
      dockerfile: dockerfile-pgsync
    command: >
      sh -c "bootstrap --config schema.json && pgsync --config schema.json -d"
    sysctls:
      - net.ipv4.tcp_keepalive_time=200
      - net.ipv4.tcp_keepalive_intvl=200
      - net.ipv4.tcp_keepalive_probes=5
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
      elasticsearch:
        condition: service_healthy
    environment:
      - PG_USER=${POSTGRES_USER}
      - PG_HOST=postgres
      - PG_PASSWORD=${POSTGRES_PASSWORD}
      - LOG_LEVEL=INFO
      - ELASTICSEARCH_PORT=9200
      - ELASTICSEARCH_SCHEME=http
      - ELASTICSEARCH_HOST=elasticsearch
      - REDIS_HOST=redis
      - REDIS_AUTH=${REDIS_PASSWORD}
```

2. В `dockerfile-pg` добавить

```dockerfile
RUN echo "listen_addresses = '*'" >> /opt/bitnami/postgresql/conf/conf.d/extended.conf
RUN echo "max_replication_slots = 10" >> /opt/bitnami/postgresql/conf/conf.d/extended.conf
RUN echo "wal_level = logical" >> /opt/bitnami/postgresql/conf/conf.d/extended.conf
```

3. Добавить папку `pgsync`, скопировать туда `dockerfile-pgsync`
4. Если на промежуточной таблице для связи many-to-many не задан первичный ключ - нужно его задать и убедиться что он есть после всех миграций [пример](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/PGSync/migrations/V1.1.1__initialize.sql#L21)
5. В папку `pgsync` добавить схему `schema.json`, соответствующую структуре таблиц проекта [пример](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/PGSync/pgsync/schema.json) [документация](https://pgsync.com/schema/)
