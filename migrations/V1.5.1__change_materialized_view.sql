drop materialized view if exists company_worker_link;

alter table company 
	drop column if exists founded,
    drop column if exists enterprise_value; 
        
alter table company 
	add column founded int,
	add column enterprise_value int;

comment on column company.enterprise_value is '(million euro)';

UPDATE company
    SET founded = (case when title = 'Coppa-Coulla' then 1989
                       when title = 'South Wind' then 2007
                       when title = 'MooV' then 2000
                       when title = 'Icing On The Cake' then 2013
                       when title = 'Herb' then 1980
                   end),
        enterprise_value = (case when title = 'Coppa-Coulla' then 2000
		                       when title = 'South Wind' then 1050
		                       when title = 'MooV' then 820
		                       when title = 'Icing On The Cake' then 345
		                       when title = 'Herb' then 660
                            end);

create
materialized view company_worker_link as
select co.id as c_id, co.title, co.founded, co.enterprise_value, co.field, 
wk.id as w_id, wk.f_name, wk.s_name, wk.age, wk.education
from company as co
left join company_worker on co.id = company_worker.company_id
left join worker as wk on wk.id = company_worker.worker_id;

drop index if exists company_worker_link_id;
create unique index company_worker_link_id on company_worker_link (c_id, w_id);

drop index if exists company_worker_link_btree;
create index company_worker_link_btree on company_worker_link
using btree (age, founded, enterprise_value);
