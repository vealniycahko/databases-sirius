drop index if exists worker_search_by_age;
create index worker_search_by_age on worker
using btree (age);
