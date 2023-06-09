# Сборка приложения:
```bash
docker compose up --build
```

# Запросы:
```bash
# получить все компании с работниками
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/companies?offset=0&limit=100'
# создание компании
curl --location --request POST 'http://127.0.0.1:{APP_PORT}/companies/create' --header 'Content-Type: application/json' --data-raw '{"title":"MyNee", "founded":2010, "field":"Banking"}'
# обновить название компании по id
curl --location --request POST 'http://127.0.0.1:{APP_PORT}/companies/update' --header 'Content-Type: application/json' --data-raw '{"id":"", "title":"Diamond"}'
# удалить компанию по id
curl --location --request DELETE 'http://127.0.0.1:{APP_PORT}/companies/delete' --header 'Content-Type: application/json' --data-raw '{"id":""}'
# получение возрастной гистограммы работников
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/age_histogram'
# выборка работников по диапазону возрастов с реплики
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/index_search' --header 'Content-Type: application/json' --data-raw '{"age_from":30, "age_to":40}'
# выборка из материализованного представления с помощью индекса (по возрасту работника, дате основания и стоимости компании)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/mat_view/index_search' --header 'Content-Type: application/json' --data-raw '{"age_from":30, "age_to":60, "founded_from":1990, "founded_to":2020, "ent_value_from":200, "ent_value_to":900}'
# поиск работников по должности (поиск по атрибуту типа jsonb)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/json_position' --header 'Content-Type: application/json' --data-raw '{"position": "middle"}'
# поиск компаний по филиалу в городе (поиск по атрибуту типа text[])
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/companies/array_search' --header 'Content-Type: application/json' --data-raw '{"city": "Stockholm"}'
# поиск работников по образованию (pgsync, elasticsearch)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/match_search?education=College'
# max, min avg, total возраст работников (pgsync, elasticsearch)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/aggregations'
# поиск компаний по назвинию с ошибками, окончаниями и по синонимам (pgsync, elasticsearch)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/companies/synonym_search?title=grass'
# поиск по именам работников (autocomplete)
http://127.0.0.1:{APP_PORT}
# общий возраст работников с группировкой по образованию (clickhouse)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/workers/agg_by_education'
# стоимость компаний, основанных после 2000 года (clickhouse)
curl --location --request GET 'http://127.0.0.1:{APP_PORT}/companies/founded_range'
```