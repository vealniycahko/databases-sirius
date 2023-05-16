import psycopg2

from typing import List
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(database='', user='', password='', host='localhost', port=5432,
                        cursor_factory=RealDictCursor)

class Folder:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.size = None
        self.parent = None
        self.childrens: List[Folder] = []
        self.files: List[File] = []

    def files_size(folder):
        total = 0
        for file in folder.files:
            total += file.size
        return total

    def f_size(self):
        total = 0
        total += self.files_size()
        for folder in self.childrens:
            total += folder.f_size()
        return total

class File:
    def __init__(self, id: int, name: str, size: int):
        self.id = id
        self.name = name
        self.size = size
        self.folder: Folder


cur = conn.cursor()

query = """
select parent.id as folder_id, parent.name as folder_name, parent.parent_id as folder_parent_id, 
child.id as child_id, child.name as child_name, child.parent_id as child_parent_id,
files.id as file_id, files.name as file_name, files.size as file_size, files.folder_id as file_folder_id
from folders as parent
    left join folders as child on parent.id = child.parent_id
	left join files on parent.id = files.folder_id;
"""

cur.execute(query)
rows = cur.fetchall()

folders_dict = {}
files_dict = {}

for row in rows:
    folder_id = row['folder_id']
    folder_name = row['folder_name']
    folder_parent_id = row['folder_parent_id'] # нужно для отношений

    folder = None
    if folder_id in folders_dict:
        tour = folders_dict[folder_id]
    else: # проверка folder_id на null не нужна, folder_id всегда != null
        folder = Folder(folder_id, folder_name)
        folders_dict[folder_id] = folder

    file_id = row['file_id']
    file_name = row['file_name']
    file_size = row['file_size']
    file_folder = row['file_folder_id'] # нужно для отношений

    file = None
    if file_id in files_dict:
        file = files_dict[file_id]
    elif file_id is not None:
        file = File(file_id, file_name, file_size)
        files_dict[file_id] = file

    # отношения folder - folder
    if folder_parent_id is not None:
        p_folder = folders_dict[folder_parent_id]
        if folder not in p_folder.childrens: 
            p_folder.childrens.append(folder)
            folder.parent = p_folder

    # отношения folder - file
    if file_folder is not None:
        f_folder = folders_dict[file_folder]
        if file not in f_folder.files: 
            f_folder.files.append(file)
            file.folder = f_folder

# вычисление folder.size
for folder in folders_dict.values():
    folder.size = folder.f_size()


folders = list(folders_dict.values())
files = list(files_dict.values())

conn.close()
