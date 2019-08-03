from .models import *

def create_test_data():
	create_clients()
	create_documents()

def is_exist(client):
	res = False
	for x in Client.objects.all():
		res = client.first_name == x.first_name and client.last_name == x.last_name and client.part_name == x.part_name
		if res:
			return res
	return res

def create_clients():
	client = Client(first_name="Дмитрий", part_name="Алексеевич", last_name="Саленый")
	if not is_exist(client):
		client.save()
	client = Client(first_name="Степан", part_name="Владимирович", last_name="Берендяев")
	client.save()
	Passport(client = client, info = {
		'документ':'пасспорт гр. РФ',
		'серия': '3345',
		'номер': '180009',
		'Пасспорт выдан':'ОТДЕЛОМ УФМС РОССИИ ПО САМАРСКОЙ ОБЛАСТИ В ГОРОДЕ МАХАЧКАЛА',
		'Фамилия':'Берендяев',
		'Имя':'Степан',
		'Отчество':'Владимирович',
		'пол':'муж.',
		'Дата рождения':'23.07.1999',
		'Место рождения':'г. Саратов Самарская обл.'
	}
			 ).save()
	client = Client(first_name="Ирина", part_name="Генадьевна", last_name="Иванова")
	if not is_exist(client):
		client.save()
	Client(first_name="Алена", part_name="Аллександровна", last_name="Голованова")
	Client(first_name="Екатерина", part_name="Евгеньевна", last_name="Герасимова")
	Client(first_name="Екатерина", part_name="Владимировна", last_name="Сычева")
	Client(first_name="Антон", part_name="Олегович", last_name="Сытник")
	Client(first_name="Антон", part_name="Владимирович", last_name="Кузнецов")

def create_documents():
	# Document(name="Credit", file_name='', file_type='pdf').save()
	# Document(name="Ipoteka", file_name='', file_type='pdf').save()
	Document(name="Справка по форме банка (сбер)", file_name='spravka_po_forme_banka.pdf', file_type='pdf').save()
	# Document(name="Spravka1", file_name='', file_type='pdf').save()
	# Document(name="Spravka3", file_name='', file_type='pdf').save()
	# Document(name="Spravka4", file_name='', file_type='pdf').save()
	# Document(name="Spravka5", file_name='', file_type='pdf').save()
def create_client_docs():
	return ''


