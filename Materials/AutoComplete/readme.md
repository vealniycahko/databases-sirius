Готовый пример со всеми нужными изменениями находится в этой папке, запуск через `docker compose up --build`

flask по адресу `http://127.0.0.1:12862` отдает страницу с примером реализации автокомплита через n-gram индекс в
ElasticSearch

Этот пример основан на
предыдущем [PGSync](https://gitlab.com/golodnyuk.iv/db_2022/-/tree/main/%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%B0%D0%BB%D1%8B%20%D0%BF%D0%BE%20%D0%BA%D1%83%D1%80%D1%81%D1%83/PGSync)
, разницу можно посмотреть
в [этом коммите](https://gitlab.com/golodnyuk.iv/db_2022/-/commit/3cc78586dc35dd33951684fd1448954a01f0d7ef)

1. Целиком скопировать файл `autocomplete.html` в папку `static`
2. Изменить `Dockerfile`, добавить `COPY static/ ./static/`
3. Добавить api метод который отдаёт страницу `autocomplete.html`:

```python
@app.route('/')
def autocomplete_page():
    try:
        return send_file('static/autocomplete.html')
    except Exception as ex:
        logging.error(repr(ex), exc_info=True)
        return {'message': 'Bad Request'}, 400
```

4. Метод поиска по n-gram индексу должен отдавать массив строк, поиск должен осуществляться по индексу из проекта:

```python
def autocomplete():
...
return jsonify(list(map(lambda hit: hit['_source']['title'], es_resp['hits']['hits'])))
```
