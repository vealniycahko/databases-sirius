Для работы примера нужно в папке с main.py создать virtual environment

Вариант для bash (ubuntu):
Нужно убедиться что стоит пакет python3.9-venv, если нет - нужно поставить через
```shell
sudo apt install python3.9-venv
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
`flask run`

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

create table equipment
(
    title text primary key,
    color text
);

create table "equipmentToHolder"
(
    "equipmentTitle" text not null references equipment on delete cascade,
    "holderPhone"    text not null references holder on delete cascade,
    unique ("equipmentTitle", "holderPhone")
);

create table "storageCell"
(
    code          text primary key,
    capacity      int not null,
    "holderPhone" text references holder on delete set null
);

insert into equipment (title, color)
values ('Ракетка', 'Красный'),
       ('Мангал', 'Красный'),
       ('Мяч', 'Белый'),
       ('Палатка', 'Серый'),
       ('Удочка', 'Чёрный'),
       ('Спальник', 'Синий'),
       ('Рюкзак', 'Зелёный'),
       ('Дождевик', 'Серый'),
       ('Компас', 'Красный'),
       ('Термос', 'Чёрный');

insert into holder (name, phone)
values ('Альберт Андреевич', '0001'),
       ('Иван Вячеславович', '0002'),
       ('Вячеслав Александрович', '0003'),
       ('Алексей Андреевич', '0004');

insert into "equipmentToHolder" ("equipmentTitle", "holderPhone")
values ('Мяч', '0001'),
       ('Рюкзак', '0001'),
       ('Мангал', '0001'),
       ('Ракетка', '0001'),
       ('Дождевик', '0001'),
       ('Удочка', '0002'),
       ('Спальник', '0002'),
       ('Ракетка', '0002'),
       ('Палатка', '0002'),
       ('Компас', '0002'),
       ('Мяч', '0003'),
       ('Ракетка', '0003'),
       ('Термос', '0003'),
       ('Палатка', '0003');

insert into "storageCell" (code, capacity, "holderPhone")
values ('YU58', 400, '0001'),
       ('NT31', 800, '0002'),
       ('AG22', 1200, '0002'),
       ('TQ66', 800, '0003');

select phone as "holderPhone", name as "holderName", "equipmentTitle", color as "equipmentColor",
       code as "storageCellCode", capacity as "storageCellCapacity"
from holder
         left join "equipmentToHolder" on phone = "equipmentToHolder"."holderPhone"
         left join equipment on "equipmentTitle" = title
         left join "storageCell" on phone = "storageCell"."holderPhone";
```
