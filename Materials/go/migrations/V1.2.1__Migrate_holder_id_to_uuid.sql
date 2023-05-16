-- начало транзакции
begin;

    
-- подключаем функцию для генерации uuid (по-умолчанию отключена)
create extension if not exists "uuid-ossp";

    
-- 1) из таблицы, которая ссылаются на holder, удаляем constraint с внешним ключом
alter table equipment_to_holder
    drop constraint equipment_to_holder_holder_id_fkey;

-- 2) переименовываем колонку со старым внешним ключом
alter table equipment_to_holder
    rename column holder_id to old_holder_id;

-- 3) добавляем колонку с новым внешним ключом
alter table equipment_to_holder
    add column holder_id uuid;


-- проделываем пункты 1-2-3 для всех таблиц, которые ссылаются на holder
alter table storage_cell
    drop constraint storage_cell_holder_id_fkey;

alter table storage_cell
    rename column holder_id to old_holder_id;

alter table storage_cell
    add column holder_id uuid;


-- в таблице holder удаляем constraint primary key
alter table holder
    drop constraint holder_pkey;

-- переименовываем колонку со старым ключом
alter table holder
    rename column id to old_id;

-- добавляем колонку с новым ключом
alter table holder
    add column id uuid default uuid_generate_v4();

/*
анонимная функция, которая циклом обходит все строки таблицы holder,
для каждой строки добавляет новый id, и всем ссылающимся на эту строку
строкам из других таблиц проставляет новый id
*/
do
$$
    declare
        row record;
    begin
        for row in select * from holder
            loop
                update equipment_to_holder set holder_id = row.id where old_holder_id = row.old_id;
                update storage_cell set holder_id = row.id where old_holder_id = row.old_id;
            end loop;
    end
$$;

-- удаляем столбец со старым id
alter table holder
    drop column old_id;
-- устанавливаем первичный ключ
alter table holder
    add primary key (id);

-- удаляем столбец со старым внешним ключом
-- удаление этой колонки так же удалит установленное ранее ограничение на уникальность
alter table equipment_to_holder
    drop column old_holder_id;
-- устанавливаем новый внешний ключ
alter table equipment_to_holder
    add constraint fk_holder_id foreign key (holder_id) references holder;
-- для связи many-to-many ставим соответствующие ограничения
alter table equipment_to_holder
    alter column holder_id set not null;
alter table equipment_to_holder
    add constraint uq_holder_id_to_equipment_id unique (holder_id, equipment_id);


-- удаляем столбец со старым внешним ключом
alter table storage_cell
    drop column old_holder_id;
        
-- устанавливаем новый внешний ключ   
alter table storage_cell
    add constraint fk_holder_id foreign key (holder_id) references holder;

-- завершение транзакции
commit;
