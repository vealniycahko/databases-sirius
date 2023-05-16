create table holder
(
    id int primary key generated always as identity,
    phone text unique,
    name  text not null
);