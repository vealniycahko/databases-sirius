drop table if exists tour cascade;
drop table if exists city cascade;
drop table if exists review cascade;
drop table if exists city_to_tour cascade;

create table tour 
(
    name text primary key,
    price numeric
);

create table city 
(
    name text primary key,
    founded text
);

create table review 
(
    id int generated always as identity primary key,
    comment text,
	ratio int,
	tourname text references tour(name)
);

create table city_to_tour
(	
	city_name text not null references city(name),
	tour_name text not null references tour(name),
	unique (city_name, tour_name)
);


insert into tour values 
	('В гостях у хаски', 20000),
    ('Хиты карелии', 12000);
      
insert into city values
	('Приозерск', '1295'),
    ('Сортавала', '1468'),
    ('Валаам', '1407');

insert into review (comment, ratio, tourname) values
	('Отличный тур!', 5, 'Хиты карелии'),
    ('Не понравилось.', 2, 'Хиты карелии');

insert into city_to_tour values
	('Приозерск', 'В гостях у хаски'),
	('Сортавала', 'В гостях у хаски'),
	('Сортавала', 'Хиты карелии'),
	('Валаам', 'Хиты карелии');
