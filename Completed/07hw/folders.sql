drop table if exists folders cascade;
drop table if exists files cascade;


create table folders
(   
    id int generated always as identity primary key,
    name text not null,
    parent_id int references folders(id)
);

create table files
(
    id int generated always as identity primary key,
    name text not null,
    size int,
    folder_id int references folders(id)
);


insert into folders (name, parent_id)
values ('Project', null),
    ('John', 1),
    ('Alice', 1),
    ('Code', 2),
    ('Images', 3);

insert into files (name, size, folder_id)
values ('Tasks.txt', 172, 2),
    ('Main.py', 2134, 4),
    ('Template.txt', 595, 3),
    ('Photo1.png', 1223, 5);
