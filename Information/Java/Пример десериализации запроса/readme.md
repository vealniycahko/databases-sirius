Даны сущности:
* Владелец со свойствами имя и телефон
* Экипировка со свойствами название и цвет
* Ячейка хранения со свойствами код и объём

Владелец может отвечать за множество разной экипировки. Экипировка может быть
распределена между несколькими владельцами.

У владельца может быть несколько ячеек хранения. Ячейка хранения 
может принадлежать только одному владельцу.

```sql
drop table if exists equipment cascade;
drop table if exists holder cascade;
drop table if exists equipment_to_holder cascade;
drop table if exists storage_cell cascade;

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

create table equipment_to_holder
(
    equipment_title text not null references equipment,
    holder_phone    text not null references holder,
    unique (equipment_title, holder_phone)
);

create table storage_cell
(
    code         text primary key,
    capacity     int not null,
    holder_phone text references holder
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

insert into equipment_to_holder (equipment_title, holder_phone)
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

insert into storage_cell (code, capacity, holder_phone)
values ('YU58', 400, '0001'),
       ('NT31', 800, '0002'),
       ('AG22', 1200, '0002'),
       ('TQ66', 800, '0003');

select phone    as holder_phone,
       name     as holder_name,
       equipment_title,
       color    as equipment_color,
       code     as storage_cell_code,
       capacity as storage_cell_capacity
from holder
         left join equipment_to_holder on phone = equipment_to_holder.holder_phone
         left join equipment on equipment_title = title
         left join storage_cell on phone = storage_cell.holder_phone;
```

Результат запроса:

| holder\_phone | holder\_name           | equipment\_title | equipment\_color | storage\_cell\_code | storage\_cell\_capacity |
|:--------------|:-----------------------|:-----------------|:-----------------|:--------------------|:------------------------|
| 0001          | Альберт Андреевич      | Дождевик         | Серый            | YU58                | 400                     |
| 0001          | Альберт Андреевич      | Ракетка          | Красный          | YU58                | 400                     |
| 0001          | Альберт Андреевич      | Мангал           | Красный          | YU58                | 400                     |
| 0001          | Альберт Андреевич      | Рюкзак           | Зелёный          | YU58                | 400                     |
| 0001          | Альберт Андреевич      | Мяч              | Белый            | YU58                | 400                     |
| 0002          | Иван Вячеславович      | Компас           | Красный          | NT31                | 800                     |
| 0002          | Иван Вячеславович      | Палатка          | Серый            | NT31                | 800                     |
| 0002          | Иван Вячеславович      | Ракетка          | Красный          | NT31                | 800                     |
| 0002          | Иван Вячеславович      | Спальник         | Синий            | NT31                | 800                     |
| 0002          | Иван Вячеславович      | Удочка           | Чёрный           | NT31                | 800                     |
| 0002          | Иван Вячеславович      | Компас           | Красный          | AG22                | 1200                    |
| 0002          | Иван Вячеславович      | Палатка          | Серый            | AG22                | 1200                    |
| 0002          | Иван Вячеславович      | Ракетка          | Красный          | AG22                | 1200                    |
| 0002          | Иван Вячеславович      | Спальник         | Синий            | AG22                | 1200                    |
| 0002          | Иван Вячеславович      | Удочка           | Чёрный           | AG22                | 1200                    |
| 0003          | Вячеслав Александрович | Палатка          | Серый            | TQ66                | 800                     |
| 0003          | Вячеслав Александрович | Термос           | Чёрный           | TQ66                | 800                     |
| 0003          | Вячеслав Александрович | Ракетка          | Красный          | TQ66                | 800                     |
| 0003          | Вячеслав Александрович | Мяч              | Белый            | TQ66                | 800                     |
| 0004          | Алексей Андреевич      | NULL             | NULL             | NULL                | NULL                    |
