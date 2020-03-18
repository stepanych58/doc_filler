import os
import sqlite3
from mainapp.mainapp.settings import *

db_path = os.path.join(BASE_DIR, "db.sqlite3")
query = os.path.join(BASE_DIR, "queries.txt")
print(query)
f = open(query,'rb')
conn = sqlite3.connect(db_path)  # или :memory: чтобы сохранить в RAM
cursor = conn.cursor()
# Создание таблицы

    # cursor.executescript(queryfile.read())
f = open (query , 'rb')
for line in f:
     insert_query = line.decode('utf8')
     print(insert_query)
     cursor.executescript(insert_query)
f.close()