В первую очередь нужно убедиться что запущен редис на порту 26596. Команда создание и запуск docker контейнера:
```shell
docker run --name redis_db2022 -p 26596:6379 -d redis --requirepass redis
```

Для работы примера нужно в папке с main.py создать virtual environment

Вариант для bash (ubuntu):
```shell
python3.9 -m venv venv
source venv/bin/activate
```

Вариант для powershell (windows):
```ps
py -m venv venv
.\venv\Scripts\activate
```

Затем нужно установить зависимости из requirements.txt
```shell
pip install -r requirements.txt
```

После этого можно запускать flask, установив перед этим следующие переменные окружения:

Вариант для bash (ubuntu):
```shell
export FLASK_APP=main.py
export FLASK_ENV=development
```

Вариант для powershell (windows):
```ps
$env:FLASK_APP=main.py
$env:FLASK_ENV=development
```

После этого можно запускать flask:
`flask run`

В данном примере есть 4 api метода, curl запросы которые им соответствуют:
```
curl --location --request GET 'http://127.0.0.1:5000/'
```
— тут отдаётся простая html страничка со счётчиком посещений.


Добавление действия пользователя:
```
curl --location --request POST 'http://127.0.0.1:5000/user_actions/add' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_name": "ivan",
    "action_name": "add_frame"
}'
```
Отмена действия пользователя:
```
curl --location --request DELETE 'http://127.0.0.1:5000/user_actions/cancel' \
--header 'Content-Type: application/json' \
--data-raw '{
    "user_name": "ivan"
}'
```
Просмотр действий пользователя:
```
curl --location --request GET 'http://127.0.0.1:5000/user_actions?user_name=ivan'
```