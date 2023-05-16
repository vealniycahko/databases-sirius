create extension pg_cron;

select cron.schedule('refresh_company_worker_link', '* * * * *',
                     $$ refresh materialized view concurrently company_worker_link $$);