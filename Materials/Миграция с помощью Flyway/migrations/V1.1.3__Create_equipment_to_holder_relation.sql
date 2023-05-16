create table equipment_to_holder
(
    equipment_id int not null references equipment on delete cascade,
    holder_id    int not null references holder on delete cascade,
    unique (equipment_id, holder_id)
);
