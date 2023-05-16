alter table worker 
	drop column if exists info;

alter table worker 
	add column info jsonb;

UPDATE worker
    SET info = (case when s_name = 'Maddison' then '[{
									"company": "Icing On The Cake",
									"position": "intern",
									"work_since": 2022
								}]'::jsonb
                     when s_name = 'Olbrighton' then '[{
									"company": "Icing On The Cake",
									"position": "middle",
									"work_since": 2015
								}]'::jsonb
                     when s_name = 'Tyler' then '[{
									"company": "Herb",
									"position": "middle",
									"work_since": 2017
								}]'::jsonb
                     when s_name = 'Stones' then '[{
									"company": "Coppa-Coulla",
									"position": "junior",
									"work_since": 2020
								},
								{
									"company": "South Wind",
									"position": "junior",
									"work_since": 2020
								},
								{
									"company": "MooV",
									"position": "junior",
									"work_since": 2021
								}]'::jsonb
                     when s_name = 'Walker' then '[{
									"company": "Coppa-Coulla",
									"position": "senior",
									"work_since": 1999
								},
								{
									"company": "Herb",
									"position": "senior",
									"work_since": 1999
								}]'::jsonb
                     when s_name = 'Bullet' then '[{
									"company": "Coppa-Coulla",
									"position": "senior",
									"work_since": 2003
								},
								{
									"company": "Herb",
									"position": "senior",
									"work_since": 2003
								}]'::jsonb
                     when s_name = 'King' then '[{
									"company": "Coppa-Coulla",
									"position": "junior",
									"work_since": 2019
								},
								{
									"company": "Herb",
									"position": "senior",
									"work_since": 2019
								}]'::jsonb
                     when s_name = 'Swanson' then '[{
									"company": "South Wind",
									"position": "middle",
									"work_since": 2009
								}]'::jsonb
                     when s_name = 'Sweet' then '[{
									"company": "MooV",
									"position": "middle",
									"work_since": 2014
								}]'::jsonb
                     when s_name = 'Stallman' then '[{
									"company": "MooV",
									"position": "middle",
									"work_since": 2017
								}]'::jsonb
                end);
                 
create index worker_info on worker using gin (info);       