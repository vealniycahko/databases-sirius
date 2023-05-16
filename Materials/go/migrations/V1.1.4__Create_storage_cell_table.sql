create table storage_cell
(
    id        int generated always as identity primary key,
    code      text unique,
    capacity  int not null,
    holder_id int references holder on delete set null
);
