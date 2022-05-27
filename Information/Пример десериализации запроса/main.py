import psycopg2

from typing import List
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database='postgres', user='postgres', password='changeme', host='localhost', port=5432,
                        cursor_factory=RealDictCursor)


class Holder:
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.equipment: List[Equipment] = []
        self.storage_cells: List[StorageCell] = []


class Equipment:
    def __init__(self, title: str, color: str):
        self.title = title
        self.color = color
        self.holders: List[Holder] = []


class StorageCell:
    def __init__(self, code: str, capacity: int):
        self.code = code
        self.capacity = capacity
        self.holder: Holder


cur = conn.cursor()

query = """
select phone as "holderPhone", name as "holderName", "equipmentTitle", color as "equipmentColor",
       code as "storageCellCode", capacity as "storageCellCapacity"
from holder
         left join "equipmentToHolder" on phone = "equipmentToHolder"."holderPhone"
         left join equipment on "equipmentTitle" = title
         left join "storageCell" on phone = "storageCell"."holderPhone";
"""
cur.execute(query)

rows = cur.fetchall()

holders_dict = {}
equipment_dict = {}
storage_cells_dict = {}
for row in rows:
    holder_phone = row['holderPhone']
    holder_name = row['holderName']

    holder = None
    if holder_phone in holders_dict:
        holder = holders_dict[holder_phone]
    # holder_phone всегда != null,
    # т.к. это левая (можно считать её главной в запросе) таблица, остальные к ней присоединяются
    # проверка holder_phone на null не нужна
    else:
        holder = Holder(holder_name, holder_phone)
        holders_dict[holder_phone] = holder

    equipment_title = row['equipmentTitle']
    equipment_color = row['equipmentColor']

    equipment = None
    if equipment_title in equipment_dict:
        equipment = equipment_dict[equipment_title]
    # дальше необходимы проверки на null значения equipment_title
    elif equipment_title is not None:
        equipment = Equipment(equipment_title, equipment_color)
        equipment_dict[equipment_title] = equipment

    storage_cell_code = row['storageCellCode']
    storage_cell_capacity = row['storageCellCapacity']
    # дальше необходимы проверки на null значения storage_cell_code
    storage_cell = None
    if storage_cell_code in storage_cells_dict:
        storage_cell = storage_cells_dict[storage_cell_code]
    elif storage_cell_code is not None:
        storage_cell = StorageCell(storage_cell_code, storage_cell_capacity)
        storage_cells_dict[storage_cell_code] = storage_cell

    # добавляем связи только если equipment_title != null
    if equipment_title is not None:
        if equipment not in holder.equipment: holder.equipment.append(equipment)
        if holder not in equipment.holders: equipment.holders.append(holder)

    # добавляем связи только если storage_cell_code != null
    if storage_cell is not None:
        if storage_cell not in holder.storage_cells: holder.storage_cells.append(storage_cell)
        storage_cell.holder = holder

holders = list(holders_dict.values())
equipment = list(equipment_dict.values())
storage_cells = list(storage_cells_dict.values())

conn.close()
