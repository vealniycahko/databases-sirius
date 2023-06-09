drop function if exists refresh_company_worker_link;
create function refresh_company_worker_link()
    returns trigger as
$$
begin
    refresh materialized view concurrently company_worker_link;

    return new;
end;
$$
    language 'plpgsql';

create trigger update_company_table
    after insert or update or delete
    on company
    for each row
execute procedure refresh_company_worker_link();