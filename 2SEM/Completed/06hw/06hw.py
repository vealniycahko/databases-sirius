class Dialogues:
    id: BIGINT,
    name: TEXT,
    t_start: TIMESTAMPTZ,
    t_finish: TIMESTAMPTZ,
    messages: List[Messages]

class Messages:
    id: BIGINT,
    content: TEXT,
    t_send: TIMESTAMPTZ,
    chat: INT,
    dialogue: None

class Questions(Messages):
    t_processing: INT

class Answers(Messages):
    channel: TEXT