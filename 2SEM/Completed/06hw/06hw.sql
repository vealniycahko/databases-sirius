DROP TABLE IF EXISTS dialogues CASCADE;
DROP TABLE IF EXISTS messages CASCADE;

CREATE TABLE dialogues
(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT,
    t_start TIMESTAMPTZ,
    t_finish TIMESTAMPTZ
);

CREATE TABLE messages
(
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    content TEXT NOT NULL,
    t_send TIMESTAMPTZ NOT NULL,
    chat INT NOT NULL REFERENCES dialogues(id),

    type text NOT NULL,
    channel TEXT,
    t_processing INT
);


INSERT INTO dialogues (name, t_start, t_finish)
VALUES ('Sell', '2016-01-01 01:02:03.123456+03', '2016-02-01 01:05:03.123456+03'),
    ('Study', '2018-01-01 20:00:00.123456+03', '2020-09-11 10:45:07.365916+03');


INSERT INTO messages (content, t_send, chat, type, t_processing)
VALUES ('Добрый день! Еще актуально?', '2016-01-01 01:02:03.123456+03', 1, 'question', 60),
    ('Отлично! Беру обе', '2016-02-01 01:02:03.123456+03', 1, 'question', 120),
    ('Добрый вечер! Могу побеспокоить?', '2018-01-01 20:00:00.123456+03', 2, 'question', 240),
    ('Не могу сложить 1 + 1...', '2018-01-01 20:10:00.123456+03', 2, 'question', 120);


INSERT INTO messages (content, t_send, chat, type, channel)
VALUES ('Здравствуйте! Да, осталось 2 штуки', '2016-01-01 01:03:03.123456+03', 1, 'answer', 'WhatsApp'),
    ('Договорились!', '2016-02-01 01:05:03.123456+03', 1, 'answer', 'WhatsApp'),
    ('Добрый! Да, без прроблем!', '2018-01-01 20:04:00.123456+03', 2, 'answer', 'Telegram'),
    ('2! Обращайтесь', '2018-01-01 20:12:00.123456+03', 2, 'answer', 'Telegram');

SELECT *
FROM dialogues
    JOIN messages ON dialogues.id = messages.chat
ORDER BY t_send;