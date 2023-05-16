Готовый пример со всеми нужными изменениями находится в этой папке, запуск через `docker compose up --build`

Во flask представлены 1 api метод на вывод всех ячеек хранения:

```shell
curl --location --request GET 'http://127.0.0.1:12862/storage_cells'
```

1. В `docker-compose.yml` добавить:

```shell
  clickhouse:
    container_name: clickhouse_pg_replication
    image: bitnami/clickhouse:22.3.15
    volumes:
      - ./clickhouse/init-replication.sh:/docker-entrypoint-initdb.d/init-click.sh
    environment:
      CLICKHOUSE_ADMIN_USER: ${CLICKHOUSE_USER}
      CLICKHOUSE_ADMIN_PASSWORD: ${CLICKHOUSE_PASSWORD}
    ports:
      - "${CLICKHOUSE_PORT}:8123"
    depends_on:
      postgres:
        condition: service_healthy
```

2. Добавить папку clickhouse, скопировать туда `init-replication.sh`
3. В `init-replication.sh` изменить названия синхронизируемых таблиц. Если название бд/пользователь/пароль отличаются от `postgres`, то изменить их в [строке подключения](https://gitlab.com/golodnyuk.iv/db_2022/-/blob/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/ClickHouse/PostgresReplication/clickhouse/init-replication.sh#L4).
