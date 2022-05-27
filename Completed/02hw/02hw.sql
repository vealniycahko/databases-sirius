drop table if exists users cascade;
drop table if exists settings cascade;

create table users
(
    nickname text primary key,
    first_name text,
    last_name text
);

create table settings
(
    font_size  int,
    color_scheme text,
    user_nickname text unique
);

alter table settings
    add foreign key (user_nickname) references users (nickname);

insert into users values
	('EXcluSiVe', 'John', 'O`Shea'),
	('shadow', 'Greg', 'Bremer'),
	('pretty_potato', 'Alice', 'Holgate');

insert into settings values
	(20, 'Dark', 'shadow'),
	(12, 'Light', 'pretty_potato'),
    (14, 'Monokai', 'EXcluSiVe');

select * from users
    join settings on nickname = user_nickname;