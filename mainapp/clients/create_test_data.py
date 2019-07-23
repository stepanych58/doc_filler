from .models import *

def create_test_data():
  create_clients()
  create_documents()
	
def create_clients():
  Client(first_name = "Дмитрий", part_name = "Алексеевич", last_name = "Саленый").save()
  Client(first_name = "Степан", part_name = "Владимирович", last_name = "Берендяев").save()
  Client(first_name = "Ирина", part_name = "Генадьевна", last_name = "Иванова").save()
  Client(first_name = "Алена", part_name = "Аллександровна", last_name = "Голованова").save()
  Client(first_name = "Екатерина", part_name = "Евгеньевна", last_name = "Герасимова").save()
  Client(first_name = "Екатерина", part_name = "Владимировна", last_name = "Сычева").save()
  Client(first_name = "Антон", part_name = "Олегович", last_name = "Сытник").save()
  Client(first_name = "Антон", part_name = "Владимирович", last_name = "Кузнецов").save()
  
def create_documents():
  Document(name = "Credit").save()
  Document(name = "Ipoteka").save()
  Document(name = "Spravka1").save()
  Document(name = "Spravka1").save()
  Document(name = "Spravka3").save()
  Document(name = "Spravka4").save()
  Document(name = "Spravka5").save()  