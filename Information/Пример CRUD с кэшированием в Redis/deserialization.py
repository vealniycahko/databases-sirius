from typing import OrderedDict


class Holder:
    def __init__(self, name: str, phone: str):
        self.name = name
        self.phone = phone
        self.equipment: list[Equipment] = []
        self.storage_cells: list[StorageCell] = []


class Equipment:
    def __init__(self, title: str, color: str):
        self.title = title
        self.color = color


class StorageCell:
    def __init__(self, code: str, capacity: int):
        self.code = code
        self.capacity = capacity


def deserialize_holders(rows: list[OrderedDict]):
    holders_dict = {}
    equipment_dict = {}
    storage_cells_dict = {}
    for row in rows:
        holder_phone = row['holderPhone']
        holder_name = row['holderName']

        holder = None
        if holder_phone in holders_dict:
            holder = holders_dict[holder_phone]
        else:
            holder = Holder(holder_name, holder_phone)
            holders_dict[holder_phone] = holder

        equipment_title = row['equipmentTitle']
        equipment_color = row['equipmentColor']

        equipment = None
        if equipment_title in equipment_dict:
            equipment = equipment_dict[equipment_title]
        elif equipment_title is not None:
            equipment = Equipment(equipment_title, equipment_color)
            equipment_dict[equipment_title] = equipment

        storage_cell_code = row['storageCellCode']
        storage_cell_capacity = row['storageCellCapacity']
        storage_cell = None
        if storage_cell_code in storage_cells_dict:
            storage_cell = storage_cells_dict[storage_cell_code]
        elif storage_cell_code is not None:
            storage_cell = StorageCell(storage_cell_code, storage_cell_capacity)
            storage_cells_dict[storage_cell_code] = storage_cell

        if equipment_title is not None:
            if equipment not in holder.equipment: holder.equipment.append(equipment)

        if storage_cell is not None:
            if storage_cell not in holder.storage_cells: holder.storage_cells.append(storage_cell)

    return list(holders_dict.values())
