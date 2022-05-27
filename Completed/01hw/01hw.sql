drop table if exists tour cascade;
drop table if exists rewiew cascade;

create table tour
(
    name text primary key,
    price numeric
);

create table rewiew
(
    comment  text,
    ratio int,
    tourname text
);

alter table rewiew
    add foreign key (tourname) references tour (name);

insert into tour values 
	('river', 12.7),
	('mountain', 11.0);

insert into rewiew (comment, ratio, tour_name) values 
	('good', 4, 'river'),
	('excellent', 5, 'river'),
    ('bad', 2, 'mountain'),
    ('very bad', 1, 'mountain');

select * from tour
    join rewiew on name = tourname;