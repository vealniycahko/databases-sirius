---create-table-----------------------------------------

drop table if exists worker;

create table worker
(
    f_name text,
    s_name text,
    age int,
    education text,
    "info.company" Array(text),
    "info.position" Array(text),
    "info.work_since" Array(int)
) engine = ReplacingMergeTree() order by (s_name);

---insert-data------------------------------------------

insert into worker (f_name, s_name, age, education, "info.company", "info.position", "info.work_since")
values ('Thomas', 'Maddison', 20, 'University of Michigan, Masters degree', ['Icing On The Cake'], ['intern'], [2022]),
       ('Maria', 'Stones', 21, 'Yale University, Bachelors degree', ['Coppa-Coulla', 'South Wind', 'MooV'], ['junior', 'junior', 'junior'], [2020, 2020, 2021]),
       ('Adam', 'Tyler', 33, 'College', ['Herb'], ['middle'], [2017]),
       ('Jeremy', 'Walker', 54, 'Columbia University, graduate student', ['Coppa-Coulla', 'Herb'], ['senior', 'senior'], [1997, 1999]),
       ('Elizabeth', 'Swanson', 36, 'College', [], [], []);
      
---nested-objects-search--------------------------------
      
select *
from worker
where has("info.company", 'Coppa-Coulla');

---nested-objects-aggregation---------------------------

select min("info.work_since")
from worker 
    array join "info.work_since";
   
---update-data------------------------------------

insert into worker (f_name, s_name, age, education, "info.company", "info.position", "info.work_since")
values ('Elizabeth', 'Swanson', 36, 'College', ['Icing On The Cake'], ['intern'], [2022]);

select * from worker final;
