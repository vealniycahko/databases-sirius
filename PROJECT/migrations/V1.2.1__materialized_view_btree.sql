drop materialized view if exists company_worker_link;

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
