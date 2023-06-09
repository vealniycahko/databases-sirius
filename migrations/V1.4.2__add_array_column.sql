alter table company 
	drop column if exists office,
	drop column if exists affiliates; 
        
alter table company 
	add column office text,
	add column affiliates text[];

UPDATE company
    SET office = (case when title = 'Coppa-Coulla' then 'Philadelphia'
                       when title = 'South Wind' then 'Antalya'
                       when title = 'MooV' then 'Kazan'
                       when title = 'Icing On The Cake' then 'Paris'
                       when title = 'Herb' then 'Kharkov'
                  end),
        affiliates = (case when title = 'Coppa-Coulla' then '{London, Tokio, Seattle, Atlanta, Phoenix}'::text[]
	                       when title = 'South Wind' then '{Barcelona, Palermo, Athens}'::text[]
	                       when title = 'MooV' then '{Krasnodar, Ekaterinburg}'::text[]
	                       when title = 'Icing On The Cake' then '{Rome, Stockholm}'::text[]
	                       when title = 'Herb' then '{Warsaw, Minsk}'::text[]
                      end);
        
create index company_affiliates on company using gin (affiliates);