drop table if exists company cascade;
drop table if exists worker cascade;
drop table if exists company_worker cascade;
drop table if exists document cascade;


create table company 
(
    id int generated always as identity primary key,
    title text not null,
    founded text,
    field text
);

create table worker 
(
    id int generated always as identity primary key,
    f_name text not null,
    s_name text not null,
    age int not null,
    education text
);

create table company_worker 
(
    company_id int not null references company(id),
    worker_id int not null references worker(id),
    unique(company_id, worker_id)
);

create table document 
(
    id int generated always as identity primary key,
    type text not null,
    information text,
    worker int not null references worker(id)
);
