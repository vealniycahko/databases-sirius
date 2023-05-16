Для работы примера нужно в папке с main.py создать virtual environment

Вариант для bash (ubuntu):
Нужно убедиться что стоит пакет python3.9-venv, если нет - нужно поставить через
```shell
apt install python3.9-venv
```
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
```shell
flask run
```

Применение миграций:
```shell
yoyo apply --database postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@host.docker.internal:${POSTGRES_PORT}/${POSTGRES_DB} ./migrations
```

В данном примере есть 4 api метода, curl запросы которые им соответствуют:
```
curl --location --request GET 'http://127.0.0.1:5000/holders?offset=1&limit=2'
```
```
curl --location --request POST 'http://127.0.0.1:5000/holders/create' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone": "0005",
    "name": "Иван Иванович"
}'
```
```
curl --location --request POST 'http://127.0.0.1:5000/holders/update' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone": "0005",
    "name": "Роман Романович"
}'
```
```
curl --location --request DELETE 'http://127.0.0.1:5000/holders/delete' \
--header 'Content-Type: application/json' \
--data-raw '{
    "phone": "0005"
}'
```

SQL код для примера:
```sql
drop table if exists equipment cascade;
drop table if exists holder cascade;
drop table if exists "equipmentToHolder" cascade;
drop table if exists "storageCell" cascade;

create table holder
(
    phone text primary key,
    name  text not null
);

insert into holder (name, phone)
values ('Альберт Андреевич', '0001'),
       ('Иван Вячеславович', '0002'),
       ('Вячеслав Александрович', '0003'),
       ('Алексей Андреевич', '0004');
```
