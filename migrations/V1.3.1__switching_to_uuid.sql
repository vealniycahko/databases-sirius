begin;

create extension if not exists "uuid-ossp";

alter table company_worker
    drop constraint company_worker_company_id_fkey;
alter table company_worker
    rename column company_id to old_company_id;
alter table company_worker
    add column company_id uuid;

alter table company
    drop constraint company_pkey;
alter table company
    rename column id to old_id;
alter table company
    add column id uuid default uuid_generate_v4();

do
$$
    declare
        row record;
    begin
        for row in select * from company
            loop
                update company_worker set company_id = row.id where old_company_id = row.old_id;
            end loop;
    end
$$;

drop materialized view if exists company_worker_link;

alter table company
    drop column old_id;
alter table company
    add primary key (id);

alter table company_worker
    drop column old_company_id;
alter table company_worker
    add constraint fk_company_id foreign key (company_id) references company;
alter table company_worker
    alter column company_id set not null;
alter table company_worker
    add constraint uq_company_id_to_worker_id unique (company_id, worker_id);

alter table company_worker
    drop constraint company_worker_worker_id_fkey;
alter table company_worker
    rename column worker_id to old_worker_id;
alter table company_worker
    add column worker_id uuid;

alter table document
    drop constraint document_worker_fkey;
alter table document
    rename column worker to old_worker;
alter table document
    add column worker uuid;

alter table worker
    drop constraint worker_pkey;
alter table worker
    rename column id to old_id;
alter table worker
    add column id uuid default uuid_generate_v4();

do
$$
    declare
        row record;
    begin
        for row in select * from worker
            loop
                update company_worker set worker_id = row.id where old_worker_id = row.old_id;
                update document set worker = row.id where old_worker = row.old_id;
            end loop;
    end
$$;

alter table worker
    drop column old_id;
alter table worker
    add primary key (id);

alter table company_worker
    drop column old_worker_id;
alter table company_worker
    add constraint fk_worker_id foreign key (worker_id) references worker;
alter table company_worker
    alter column worker_id set not null;
alter table company_worker
    add primary key (worker_id, company_id);
    
alter table document
    drop column old_worker;
alter table document
    add constraint fk_worker_id foreign key (worker) references worker;

alter table document
    drop constraint document_pkey;
alter table document
    drop column id;
alter table document
    add column id uuid default uuid_generate_v4();
alter table document
    add primary key (id);


create
materialized view company_worker_link as
select co.id as c_id, co.title, co.founded, co.field, 
wk.id as w_id, wk.f_name, wk.s_name, wk.age, wk.education
from company as co
left join company_worker on co.id = company_worker.company_id
left join worker as wk on wk.id = company_worker.worker_id;

drop index if exists company_worker_link_id;
create unique index company_worker_link_id on company_worker_link (c_id, w_id);

drop index if exists company_worker_link_btree;
create index company_worker_link_btree on company_worker_link
using btree (c_id, w_id, age);

commit;
