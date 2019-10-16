# from django.contrib.postgres.fields import JSONField
from django.db import models
from mainapp.settings import *
import jsonfield
#PDF TEMPLATE DIR
PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
#PDF GENERETED RESULT DIR
PDF_GENERATED_RESULT_DIR = STATICFILES_DIRS[3]


class Client(models.Model):
	first_name = models.CharField(max_length=30, default='Иван')
	part_name = models.CharField(max_length=30, default='Иванович')
	last_name = models.CharField(max_length=30,  default='Иванов')
	position = models.CharField(max_length=300,  default='Инженер')
	phone_number = models.CharField(max_length=10, default = '89276976453')
	email = models.EmailField(max_length=100, default = 'ivan@gmail.com')
	# class Meta:
	FAMILY_STATUS_CHOISES = [
		('not maried','не женат/не замужем'),
		('maried','женат/замужем'),
		('divorced','в разводе'),
		 ('single/widow','вдовец/вдова'),
	]
	family_status = models.CharField(choices=FAMILY_STATUS_CHOISES, max_length=13, default=FAMILY_STATUS_CHOISES[0])
	EDUCATION_STATUS_CHOISES = [
		('below the average'          ,'ниже среднего'          ),
		('the average'                ,'среднее'                ),
		('specialized secondary'      ,'второе высшее'      ),
		('incomplete higher education','незаконченное высшее образование'),
		('higher'                     ,'высшее'                     ),
		('academic degree'            ,'академическая степень'            ),
	]
	education_status = models.CharField(choices=EDUCATION_STATUS_CHOISES, max_length=50, default=EDUCATION_STATUS_CHOISES[0])
	ALL_WORK_EXPIREANCE_CHOISES = [
		('менее 1 года' ,'менее 1 года'),
		('1 - 2 года'   ,'1 - 2 года'  ),
		('2 - 5 лет'    ,'2 - 5 лет'   ),
		('более 5 лет'  ,'более 5 лет' ),
	]
	work_expireance = models.CharField(choices=ALL_WORK_EXPIREANCE_CHOISES, max_length=50, default=ALL_WORK_EXPIREANCE_CHOISES[0])

	POSITION_CATEGORY_CHOISES = [
		('руководитель среднего сзвена',       'руководитель среднего сзвена'       ),
		('Руководитель высшего звена',         'Руководитель высшего звена'         ),
		('специалист',                         'специалист'                         ),
		('рабочий',                            'рабочий'                            ),
		('высококвалифицированный специалист', 'высококвалифицированный специалист' ),
		('руководитель низшего звена',         'руководитель низшего звена'         ),
		('военносулжащий',                     'военносулжащий'                     ),
		('обслуживающий персонал',             'обслуживающий персонал'             ),
	]
	position_category = models.CharField(choices=POSITION_CATEGORY_CHOISES, max_length=50, default= POSITION_CATEGORY_CHOISES[0])
#
# 	unique_together = ('first_name', 'part_name', 'last_name',)

class Document(models.Model):
	name = models.CharField(max_length=500)
	file_name = models.CharField(max_length=500, default = "file name")
	file_type = models.CharField(max_length=20, default = "pdf")
	class_name = models.CharField(max_length=500, default = "SberPoFormeBanka")
	def get_path(self):
	    if self.file_type == 'pdf':
		    return os.path.join(PDF_TEMPLATE_DIR, self.file_name)

class ClientsFile(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    file_name = models.CharField(max_length=500, default = "clients file name")
    file_path = models.CharField(max_length=1000, default = "/")

class Passport(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	serial = models.CharField(max_length=4, default = "0000")
	number = models.CharField(max_length=6, default = "000000")
	_from = models.CharField(max_length=200, default = "отделом ФМС")
	gender = models.CharField(max_length=5, default = "м")
	bith_day = models.DateField(default="1999-01-01")
	bith_place = models.CharField(max_length=200, default = "", blank=True)
	class Meta:
		unique_together = ('client', 'serial', 'number',)

class SNILS(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	snils_number = models.CharField(max_length=20, default="123-123-123 00")

class INN(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	inn_number = models.CharField(max_length=20, default="123-123-123 00")

class Address(models.Model):
	index = models.CharField(max_length=6, default="446100")
	city = models.CharField(max_length=200, default="Самара")
	street = models.CharField(max_length=200, default="Николая-Панова")
	buildingNumber = models.CharField(max_length=6, default="144")
	housing = models.CharField(max_length=6,default="",blank=True)
	structure = models.CharField(max_length=6,default="",blank=True)
	flat = models.CharField(max_length=6, default="25",blank=True)

class PostAddress(models.Model):
	index = models.CharField(max_length=6, default="446100")
	city = models.CharField(max_length=200, default="Самара")
	street = models.CharField(max_length=200, default="Николая-Панова")
	buildingNumber = models.CharField(max_length=6, default="144")
	housing = models.CharField(max_length=6,default="",blank=True)
	structure = models.CharField(max_length=6,default="",blank=True)
	flat = models.CharField(max_length=6, default="25",blank=True)

class BankDetail(models.Model):
	account_number = models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True)
	correspondent_account_number =models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True)
	bic = models.CharField(max_length=11, default='000 000 000', blank=True)
	bank_name = models.CharField(max_length=1000, default='ОАО Сбербанк', blank=True)
# Bank Account Number: (20 digits)
# Correspondent account number: (20 digits) BIC: (9 digits)
# Name of the bank in which the current account is open:

class OrganizationInfo(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True
	)
	address = models.ForeignKey(
		Address,
		on_delete=models.CASCADE,
	)
	post_address = models.ForeignKey(
		PostAddress,
		on_delete=models.CASCADE,
	)
	bank_detail = models.ForeignKey(
		BankDetail,
		on_delete=models.CASCADE,
	)
	full_name = models.CharField(max_length=10000, default='Сбербанк')
	accountent_number = models.CharField(max_length=10, default='1345678911')
	hr_number = models.CharField(max_length=10, default='1345678911')
	inn_number = models.CharField(max_length=100, default='1345678911')
	field_of_activity = models.CharField(max_length=100, default='IT')
	EMPLOYMENT_TYPE_CHOISES = [
	'hire',
	'Privte buisness',
	'lawyer',
	'notary',
	'business owner',
	# ( in this case	indicate	the	size	of	the	share(string)), I
	'do not work',
	]
	INCORPARATION_FORM_CHOISES = [
		'ООО',
		'ПАО',
		'ЗАО\АО',
		'гос.учреждение',
		'иное(здесь строка)',
	]
	NUMBER_OF_STAFF_CHOISES = [
		'до 10',
		'10-100',
		'101-500',
		'более 500',
	]
	WORK_EXPERIENCE_CHOISES = [
		'до 4 мес',
		'4 - 6 мес',
		'от 6 мес',
		'до 1 года',
		'1 - 2 года',
		'2 - 5 лет',
		'более 5 лет',
	]
# class EmployeeIncomeInfo(models.Model):
# СРЕДНЕМЕСЯЧНЫЙ ДОХОД ЗА ПОСЛЕДНИЕ МЕСЯЦЕВ2 (указывается 6 месяцев; если стаж работы меньше 6 месяцев, указывается
# фактическое количество месяцев, за которые произведен расчет, и среднемесячный доход за фактически отработанные месяцы):
# Цифрами Международный код валюты
# Прописью
# СРЕДНЕМЕСЯЧНЫЙ РАЗМЕР НАЛОГА НА ДОХОДЫ ФИЗИЧЕСКИХ ЛИЦ ЗА ПОСЛЕДНИЕ МЕСЯЦЕВ (указывается 6 месяцев; если
# стаж работы меньше 6 месяцев, указывается фактическое количество месяцев, за которые произведен расчет, и среднемесячный размер налога
# за фактически отработанные месяцы):
# Цифрами Международный код валюты
# Прописью