DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS twits CASCADE;
DROP TABLE IF EXISTS subscribtions CASCADE;

CREATE TABLE users
(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    username TEXT NOT NULL,
    mail TEXT
);

CREATE TABLE twits
(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    published TIMESTAMPTZ,
    owner BIGINT REFERENCES users(id)
);

CREATE TABLE subscribtions
(
    who BIGINT NOT NULL REFERENCES users(id),
    to_whom BIGINT NOT NULL REFERENCES users(id),
    UNIQUE (who, to_whom)
);

INSERT INTO users (username, mail)
VALUES ('plushka', 'writetome@gmail.com'),
    ('wildCow', 'wild.cow@mail.ru'),
    ('antoninho', 'anton.sapogov@gmail.com'),
    ('123four5', 'daetoya@yandex.ru'),
    ('John L.', 'postforwork@gmail.com');

INSERT INTO twits (content, published, owner)
VALUES ('Wonderful day!', '2020-07-20 11:23:42.322315+02', 2),
    ('I am going crazy...', '2021-04-09 18:42:59.927402+03', 3);

INSERT INTO subscribtions (who, to_whom)
VALUES (1, 2),
    (1, 3),
    (4, 1),
    (5, 1);

SELECT main.id, main.username, main.mail, outt.to_whom, twits.id, 
twits.content, twits.published, rely.id, rely.username, rely.mail
FROM users AS main
    JOIN subscribtions AS outt ON main.id = outt.who
    JOIN subscribtions AS inn ON main.id = inn.to_whom
    LEFT JOIN twits ON outt.to_whom = twits.owner
    LEFT JOIN users AS rely ON inn.who = rely.id
WHERE main.id = 1;