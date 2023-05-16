package org.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Properties;

class Holder {
    String name;
    String phone;
    ArrayList<Equipment> equipment = new ArrayList<>();
    ArrayList<StorageCell> storageCells = new ArrayList<>();

    public Holder(String name, String phone) {
        this.name = name;
        this.phone = phone;
    }
}

class Equipment {
    String title;
    String color;
    ArrayList<Holder> holders = new ArrayList<>();

    public Equipment(String title, String color) {

        this.title = title;
        this.color = color;
    }

    public Equipment() {
    }
}

class StorageCell {
    String code;
    int capacity;
    Holder holder;

    public StorageCell(String code, int capacity) {
        this.code = code;
        this.capacity = capacity;
    }

    public StorageCell() {
    }
}

public class Main {
    public static void main(String[] args) {
        Properties connectionProps = new Properties();
        connectionProps.put("user", "postgres");
        connectionProps.put("password", "123");
        String url = "jdbc:postgresql://127.0.0.1:5432/postgres";
        Connection conn;
        Statement stmt;

        var query = """
                select phone    as holder_phone,
                       name     as holder_name,
                       equipment_title,
                       color    as equipment_color,
                       code     as storage_cell_code,
                       capacity as storage_cell_capacity
                from holder
                         left join equipment_to_holder on phone = equipment_to_holder.holder_phone
                         left join equipment on equipment_title = title
                         left join storage_cell on phone = storage_cell.holder_phone;
                """;

        try {
            conn = DriverManager.getConnection(url, connectionProps);
            stmt = conn.createStatement();

            var rs = stmt.executeQuery(query);
            var holdersDict = new HashMap<String, Holder>();
            var equipmentDict = new HashMap<String, Equipment>();
            var storageCellDict = new HashMap<String, StorageCell>();
            while (rs.next()) {
                var holderPhone = rs.getString("holder_phone");
                var holderName = rs.getString("holder_name");
                var equipmentTitle = rs.getString("equipment_title");
                var equipmentColor = rs.getString("equipment_color");
                var storageCellCode = rs.getString("storage_cell_code");
                var storageCellCapacity = rs.getInt("storage_cell_capacity");

                Holder holder;
                if (holdersDict.containsKey(holderPhone)) {
                    holder = holdersDict.get(holderPhone);
                } else {
                    holder = new Holder(holderName, holderPhone);
                    holdersDict.put(holderPhone, holder);
                }

                var equipment = new Equipment();
                if (equipmentDict.containsKey(equipmentTitle)) {
                    equipment = equipmentDict.get(equipmentTitle);
                } else if (equipmentTitle != null) {
                    equipment = new Equipment(equipmentTitle, equipmentColor);
                    equipmentDict.put(equipmentTitle, equipment);
                }

                var storageCell = new StorageCell();
                if (storageCellDict.containsKey(storageCellCode)) {
                    storageCell = storageCellDict.get(storageCellCode);
                } else if (storageCellCode != null) {
                    storageCell = new StorageCell(storageCellCode, storageCellCapacity);
                    storageCellDict.put(storageCellCode, storageCell);
                }

                if (equipmentTitle != null) {
                    if (holder.equipment.stream().noneMatch(eq -> equipmentTitle.equals(eq.title))) {
                        holder.equipment.add(equipment);
                    }

                    if (equipment.holders.stream().noneMatch(h -> holderPhone.equals(h.phone))) {
                        equipment.holders.add(holder);
                    }
                }

                if (storageCellCode != null) {
                    if (holder.storageCells.stream().noneMatch(sc -> storageCellCode.equals(sc.code))) {
                        holder.storageCells.add(storageCell);
                    }
                    storageCell.holder = holder;
                }
            }

            var holders = holdersDict.values();
            var equipments = equipmentDict.values();
            var storageCells = storageCellDict.values();
            System.out.println();
        } catch (Exception ex) {
            System.out.println(ex.getMessage());
        }
    }
}
