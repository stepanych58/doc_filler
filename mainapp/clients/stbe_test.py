# class T1():
#      r = '1234';
#      def do(self):
#           return 'do'

# print("start")
# # obj = T1();
# # a1 = 'r' in dir(obj)
# # print(a1)
# # # print(dir(obj))
# # print(obj.__dir__())
# # print(obj.__dict__)
# # print(obj.__getattribute__('r'))
# # print("end")






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











# что то что было, неизвестно зачем
# import os
# from mainapp.mainapp.settings import *
# from django.contrib.auth.models import User
# for file in os.listdir(STATIC_DIR):
#     if file:
#         print(os.path.join(STATIC_DIR, file))


# user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
# user.first_name = 'John'
# user.last_name = 'Citizen'
# user.save()