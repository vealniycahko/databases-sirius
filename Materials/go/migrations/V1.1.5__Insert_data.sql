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

insert into equipment_to_holder
values (3, 1),
       (7, 1),
       (2, 1),
       (1, 1),
       (8, 1),
       (5, 2),
       (6, 2),
       (1, 2),
       (4, 2),
       (9, 2),
       (3, 3),
       (1, 3),
       (10, 3),
       (4, 3);

insert into storage_cell (code, capacity, holder_id)
values ('YU58', 400, 1),
       ('NT31', 800, 2),
       ('AG22', 1200, 2),
       ('TQ66', 800, 3);
