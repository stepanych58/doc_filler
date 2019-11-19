# from django.contrib.postgres.fields import JSONField
from django.db import models
from mainapp.settings import *
import jsonfield

# PDF TEMPLATE DIR
PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
# PDF GENERETED RESULT DIR
PDF_GENERATED_RESULT_DIR = STATICFILES_DIRS[3]

YES_NO_CHOISES = [
	('yes', 'да'),
	('no', 'нет'),
]

WORK_EXPERIENCE_CHOISES = [
	('1', 'до 4 мес'),
	('2', '4 - 6 мес'),
	('3', 'от 6 мес'),
	('4', 'до 1 года'),
	('5', '1 - 2 года'),
	('6', '2 - 5 лет'),
	('7', 'более 5 лет'),
]

POSITION_CATEGORY_CHOISES = [
	('руководитель среднего сзвена', 'руководитель среднего сзвена'),
	('Руководитель высшего звена', 'Руководитель высшего звена'),
	('специалист', 'специалист'),
	('рабочий', 'рабочий'),
	('высококвалифицированный специалист', 'высококвалифицированный специалист'),
	('руководитель низшего звена', 'руководитель низшего звена'),
	('военносулжащий', 'военносулжащий'),
	('обслуживающий персонал', 'обслуживающий персонал'),
]


class Client(models.Model):
	first_name = models.CharField(max_length=30, default='Иван')
	part_name = models.CharField(max_length=30, default='Иванович')
	last_name = models.CharField(max_length=30, default='Иванов')
	position = models.CharField(max_length=300, default='Инженер')
	phone_number = models.CharField(max_length=12, default='89276976453')
	email = models.EmailField(max_length=100, default='ivan@gmail.com')


#
# 	unique_together = ('first_name', 'part_name', 'last_name',)

class Document(models.Model):
	name = models.CharField(max_length=500)
	file_name = models.CharField(max_length=500, default="file name")
	file_type = models.CharField(max_length=20, default="pdf")
	class_name = models.CharField(max_length=500, default="SberPoFormeBanka")

	def get_path(self):
		if self.file_type == 'pdf':
			return os.path.join(PDF_TEMPLATE_DIR, self.file_name)


class ClientsFile(models.Model):
	client = models.ForeignKey(Client, on_delete=models.CASCADE)
	file_name = models.CharField(max_length=500, default="clients file name")
	file_path = models.CharField(max_length=1000, default="/")


class Passport(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	serial = models.CharField(max_length=4, default="0000")
	number = models.CharField(max_length=6, default="000000")
	_from = models.CharField(max_length=200, default="отделом ФМС")
	gender = models.CharField(max_length=5, default="м")
	birthday = models.DateField(default="1999-01-01")
	# date_of = models.DateFiled(default="1999-01-01")
	code_of = models.CharField(max_length=8, default="344-222")

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
	housing = models.CharField(max_length=6, default="", blank=True)
	structure = models.CharField(max_length=6, default="", blank=True)
	flat = models.CharField(max_length=6, default="25", blank=True)
	oblast = models.CharField(max_length=200, default="Самарская обл.", blank=True)
	rayon = models.CharField(max_length=200, default="Волжский р-он.", blank=True)


class PostAddress(models.Model):
	index = models.CharField(max_length=6, default="446100")
	city = models.CharField(max_length=200, default="Самара")
	street = models.CharField(max_length=200, default="Николая-Панова")
	buildingNumber = models.CharField(max_length=6, default="144")
	housing = models.CharField(max_length=6, default="", blank=True)
	structure = models.CharField(max_length=6, default="", blank=True)
	flat = models.CharField(max_length=6, default="25", blank=True)
	oblast = models.CharField(max_length=200, default="Самарская обл.", blank=True)
	rayon = models.CharField(max_length=200, default="Волжский р-он.", blank=True)


class BankDetail(models.Model):
	account_number = models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True)
	correspondent_account_number = models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True)
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
	INCORPARATION_FORM_CHOISES = [
		('1', 'ООО'),
		('2', 'ПАО'),
		('3', 'ЗАО\АО'),
		('4', 'гос.учреждение'),
		('5', 'иное(здесь строка)'),
	]
	incorparation_form = models.CharField(choices=INCORPARATION_FORM_CHOISES, max_length=13,
										  default=INCORPARATION_FORM_CHOISES[0])
	NUMBER_OF_STAFF_CHOISES = [  # числеенность сотрудников
		('1', 'до 10'),
		('2', '10-100'),
		('3', '101-500'),
		('4', 'более 500'),
	]
	number_of_staff = models.CharField(choices=NUMBER_OF_STAFF_CHOISES, max_length=13,
									   default=NUMBER_OF_STAFF_CHOISES[0])
	work_experience = models.CharField(choices=WORK_EXPERIENCE_CHOISES, max_length=13,
									   default=WORK_EXPERIENCE_CHOISES[0])


class AdditionalClientInfo(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True
	)
	СREDIT_TYPE_CHOISES = [
		('1', 'готовое жилье'),
		('2', 'рефинансирование'),
		('3', 'строящееся жилье'),
		('4', 'под залог недвижимости'),
	]
	PROPERTY_TYPE = [  # тип имущества квартира, апартаменты, таунхаус, жилой дом с участком
		('1', 'квартира'),
		('2', 'апартаменты'),
		('3', 'таунхаус'),
		('4', 'жилой дом с участком'),
	]
	REGISTRATION_TYPES = [
		('1', 'постоянная'),
		('2', 'временная'),
	]
	product = models.CharField(choices=СREDIT_TYPE_CHOISES, max_length=50, default=СREDIT_TYPE_CHOISES[0])
	property = models.CharField(choices=PROPERTY_TYPE, max_length=50, default=PROPERTY_TYPE[0])
	full_insurance = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									  default=YES_NO_CHOISES[0])  # полное страхование
	registration = models.CharField(choices=REGISTRATION_TYPES, max_length=50,
									default=REGISTRATION_TYPES[0])  # полное страхование
	address_of_registration = models.CharField(max_length=10000, default='Адрес регистрации (постоянная/временная)')
	actual_address = models.CharField(max_length=10000, default='Адрес фактического проживания')
	count_of_children = models.CharField(max_length=2, default="0")  # количество детей
	# class Meta:
	FAMILY_STATUS_CHOISES = [
		('not maried', 'не женат/не замужем'),
		('maried', 'женат/замужем'),
		('divorced', 'в разводе'),
		('single/widow', 'вдовец/вдова')
	]
	family_status = models.CharField(choices=FAMILY_STATUS_CHOISES, max_length=13, default=FAMILY_STATUS_CHOISES[0])
	EDUCATION_STATUS_CHOISES = [
		('below the average', 'ниже среднего'),
		('the average', 'среднее'),
		('specialized secondary', 'второе высшее'),
		('incomplete higher education', 'незаконченное высшее образование'),
		('higher', 'высшее'),
		('academic degree', 'академическая степень'),
	]
	education_status = models.CharField(choices=EDUCATION_STATUS_CHOISES, max_length=50,
										default=EDUCATION_STATUS_CHOISES[0])
	ALL_WORK_EXPIREANCE_CHOISES = [
		('1', 'менее 1 года'),
		('2', '1 - 2 года'),
		('3', '2 - 5 лет'),
		('4', 'более 5 лет'),
	]
	work_expireance = models.CharField(choices=ALL_WORK_EXPIREANCE_CHOISES, max_length=50,
									   default=ALL_WORK_EXPIREANCE_CHOISES[0])
	position_category = models.CharField(choices=POSITION_CATEGORY_CHOISES, max_length=50,
										 default=POSITION_CATEGORY_CHOISES[0])
	WORK_TYPES = [
		# тип занятости: по найму, ИП, адвокат, нотариус, собственник бизнеса (в этом случае указать размеро доли(строка)), не работаю
		('1', 'по найму'),
		('2', 'ИП'),
		('3', 'адвокат'),
		('4', 'собственник бизнеса'),
		('5', 'не работаю'),
	]
	work_type = models.CharField(choices=WORK_TYPES, max_length=50, default=WORK_TYPES[0])
	marriage_contract = models.CharField(choices=YES_NO_CHOISES, max_length=50,
										 default=YES_NO_CHOISES[0])  # наличие брачного договора

	# Неджимиое имущество в собственности Квартира\апартаменты, таунхаус, дом с участком, иное (здесь строка). В анкете есть 2 места. Если будет 2 заполнено, то ок, если нет - оставлю пустым
	IMMOVABLE_PROPERTY_CHOISES = [
		('1', 'Квартира'),
		('2', 'апартаменты'),
		('3', 'таунхаус'),
		('4', 'дом с участком'),
		('5', 'иное'),
	]
	immovable_property = models.CharField(choices=IMMOVABLE_PROPERTY_CHOISES, max_length=50,
										  default=IMMOVABLE_PROPERTY_CHOISES[0])

	rezident_of_usa = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									   default=YES_NO_CHOISES[0])  # Являетесь ли вы налоговым резидентом США
	rezident_of_other_goverment = models.CharField(choices=YES_NO_CHOISES, max_length=50,
												   default=YES_NO_CHOISES[
													   0])  # Являетесь ли вы налоговым резидентом другого государства за исключением США
	foreign_citizen = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									   default=YES_NO_CHOISES[0])  # Являетесь ли вы иностранным гражданином

	additional_work = models.CharField(choices=WORK_TYPES, max_length=50,
									   default=WORK_TYPES[0])  # работа по совместительству
	additional_work_expireance = models.CharField(choices=WORK_EXPERIENCE_CHOISES, max_length=50,
												  default=WORK_EXPERIENCE_CHOISES[0])
	additional_work_category = models.CharField(choices=POSITION_CATEGORY_CHOISES, max_length=50,
												default=POSITION_CATEGORY_CHOISES[0])
	income_of_main_work = models.CharField(max_length=200, default="доход от основной работы")
	income_of_additional_work = models.CharField(max_length=200, default="доход от работы по совместительству")
	mark_of_car = models.CharField(max_length=200, default="марка авто ")
	year_of_manufacture_of_car = models.CharField(max_length=200, default="год выпуска авто")
	car_valuation = models.CharField(max_length=200, default="оценка стоимости авто")
	car_valuation = models.CharField(max_length=200, default="оценка стоимости авто")
	market_value_of_real_estate = models.CharField(max_length=200, default="Рыночная стоимость недвижимости")
	average_income = models.CharField(max_length=200, default="средний доход до вычета налогов")  # Это я воткнул
	aliment = models.CharField(max_length=200, default="Алименты")  # Это я воткнул
	monetary_obligations = models.CharField(max_length=200,
											default="Совокупные ежемесячные обязательства (за исключением алиментов)")  # Это я воткнул

# WORK_TYPES = [ #тип занятости: по найму, ИП, адвокат, нотариус, собственник бизнеса (в этом случае указать размеро доли(строка)), не работаю
# 	('1',''),
# 	('2',''),
# 	('3',''),
# 	('4',''),
# 	('5',''),
# ]

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
