create table holder
(
    id    int generated always as identity primary key,
    phone text unique,
    name  text not null
);
