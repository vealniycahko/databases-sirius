insert into company (title, founded, field) values
    ('Coppa-Coulla', 'September, 1989', 'Drinks'),
    ('South Wind', 'April, 2007', 'Hotels'),
    ('MooV', 'January, 2000', 'Shipping'),
    ('Icing On The Cake', 'July, 2013', 'Restaurant'),
    ('Herb', 'December, 1980', 'Farm');

insert into worker (f_name, s_name, age, education) values
    ('Thomas', 'Maddison', 20, 'University of Michigan, Masters degree'),
    ('Alice', 'Olbrighton', 42, 'Duke University, Bachelors degree'),
    ('Adam', 'Tyler', 33, 'College'),
    ('Maria', 'Stones', 21, 'Yale University, Bachelors degree'),
    ('Jeremy', 'Walker', 54, 'Columbia University, graduate student'),
    ('Nick', 'Bullet', 65, 'School'),
    ('Antony', 'King', 27, 'Dartmouth College'),
    ('Elizabeth', 'Swanson', 36, 'College'),
    ('Pol', 'Sweet', 48, 'School'),
    ('Karolin', 'Stallman', 24, 'University of Miami, Masters degree');

insert into company_worker values
    (1, 4),
    (1, 5),
    (1, 6),
    (1, 7),
    (2, 4),
    (2, 8),
    (3, 4),
    (3, 9),
    (3, 10),
    (4, 1),
    (4, 2),
    (5, 3),
    (5, 5),
    (5, 6),
    (5, 7);

insert into document (type, information, worker) values
    ('Military ID', 'Not fit', 1),
    ('The Volunteers Book', '40 hours', 2),
    ('College Diploma', 'Exellent', 3),
    ('The Volunteers Book', '55 hours', 4),
    ('University Diploma', 'Good', 4),
    ('Military ID', 'Received', 5),
    ('University Diploma', 'Exellent', 5),
    ('Medical Book', 'Normal', 6),
    ('Military ID', 'Not fit', 7),
    ('College Diploma', 'Good', 8),
    ('Military ID', 'Postponement', 9),
    ('The Volunteers Book', '32 hours', 10),
    ('Medical Book', 'Normal', 10);
