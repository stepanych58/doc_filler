from django.db import models
from mainapp.settings import *
from django.contrib.auth.models import User

# PDF TEMPLATE DIR
from .choises import *

PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
# PDF GENERETED RESULT DIR
PDF_GENERATED_RESULT_DIR = STATICFILES_DIRS[3]

class Client(models.Model):
	# author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)
	first_name = models.CharField(max_length=30, default='Иван')
	part_name = models.CharField(max_length=30, default='Иванович')
	last_name = models.CharField(max_length=30, default='Иванов')

class Author(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', blank=True, null=True)


class Approver(models.Model):
	a_first_name = models.CharField(max_length=30, default='Иван')
	a_part_name = models.CharField(max_length=30, default='Иванович')
	a_last_name = models.CharField(max_length=30, default='Иванов')
	a_phone_number = models.CharField(max_length=12, default='89276976453')  # телефон
	a_position = models.CharField(max_length=300, default='Инженер')  # должность
	a_email_v = models.CharField(max_length=300, default='Инженер')  # должность


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


class Address(models.Model):
	index = models.CharField(max_length=6, default="446100", null = True)  # индекс
	country = models.CharField(max_length=200, default="Россия", blank=True, null = True)  # страна
	oblast = models.CharField(max_length=200, default="Самарская обл.", blank=True, null = True)  # область/республика/край
	rayon = models.CharField(max_length=200, default="Волжский р-он.", blank=True, null = True)  # район
	city = models.CharField(max_length=200, default="Самара", null = True)  # город/поселок
	street = models.CharField(max_length=200, default="Николая-Панова", null = True)  # улица
	buildingNumber = models.CharField(max_length=6, default="144", null = True)  # номер дома
	housing = models.CharField(max_length=6, default="", blank=True, null = True)  # корпус
	structure = models.CharField(max_length=6, default="", blank=True, null = True)  # строение
	flat = models.CharField(max_length=6, default="25", blank=True, null = True)  # квартира/офис
	basis_of_residence = models.CharField(max_length=6, default="Зарегистрирован", blank=True, null = True)  # основание проживания
	is_post_addr = models.CharField(choices=YES_NO_CHOISES, max_length=50, default=YES_NO_CHOISES[1], blank=True, null = True)

class Passport(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	serial = models.CharField(max_length=4, default="0000")
	number = models.CharField(max_length=6, default="000000")
	v_from = models.CharField(max_length=200, default="отделом ФМС")  # кем выдан
	gender = models.CharField(GENDER_CHOISES, max_length=3, default=GENDER_CHOISES[0])  # пол
	birthday = models.DateField(default="1999-01-01")
	date_of = models.DateField(default="1999-01-01")  # дата выдачи
	code_of = models.CharField(max_length=8, default="344-222")
	registration_address = models.ForeignKey(
		Address,
		on_delete=models.CASCADE
	)
	class Meta:
		unique_together = ('client', 'serial', 'number',)


class BankDetail(models.Model):
	account_number = models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True, null = True)
	correspondent_account_number = models.CharField(max_length=24, default='0000 0000 0000 0000 0000', blank=True, null = True)
	bic = models.CharField(max_length=11, default='000 000 000', blank=True, null = True)
	bank_name = models.CharField(max_length=1000, default='ОАО Сбербанк', blank=True, null = True)

class JobInfo(models.Model):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE,
		primary_key=False
	)
	is_general = models.CharField(choices=YES_NO_CHOISES, max_length=4,
								  default=YES_NO_CHOISES[0], null = True)  # основное место работы(да, нет)
	full_name = models.CharField(max_length=200, default="Пятёрочка", null = True)
	address = models.ForeignKey(
		Address,
		related_name='address_rn',
		on_delete=models.CASCADE, null = True
	)
	post_address = models.ForeignKey(
		Address,
		related_name='post_address_rn',
		on_delete=models.CASCADE, null = True
	)
	inn_number = models.CharField(max_length=100, default='1345678911', null = True)  # Инн
	bank_detail = models.ForeignKey(
		BankDetail,
		on_delete=models.CASCADE, null = True
	)
	account_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # телефон бугалтерии
	hr_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # телефон отдела кадров
	work_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # рабочий телефон
	age = models.CharField(max_length=3, default='10', null = True)  # возраст организации
	number_of_staff = models.CharField(choices=NUMBER_OF_STAFF_CHOISES, max_length=13,
									   default=NUMBER_OF_STAFF_CHOISES[0], null = True)  # количество сотрудников (сделать селект)
	work_experience = models.CharField(choices=WORK_EXPERIENCE_CHOISES, max_length=13,
									   default=WORK_EXPERIENCE_CHOISES[0], null = True)  # стаж в данной организации
	site = models.CharField(max_length=100, default='google.com', null = True)  # сайт организации
	position = models.CharField(max_length=300, default='Инженер', null = True)  # должность
	position_category = models.CharField(choices=POSITION_CATEGORY_CHOISES, max_length=200,
										 default=POSITION_CATEGORY_CHOISES[0], null = True)  # категория должности
	salary = models.CharField(max_length=3, default='10', null = True)  # доход до налогооблажения
	is_probation = models.CharField(choices=YES_NO_CHOISES, max_length=200,
									default=YES_NO_CHOISES[0], null = True)  # испытательный срок(да, нет)
	kind_of_contract = models.CharField(choices=KINDS_OF_CONTRACT, max_length=200,
										default=KINDS_OF_CONTRACT[0], null = True)  # Вид договора (Понайму, бессрочный, по найму срочный)
	contract_start = models.DateField(default="2000-01-01", null = True)  # дата заключения договора
	contract_end = models.DateField(default="2000-01-01", null = True)  # дата окончания договора
	incorparation_form = models.CharField(choices=INCORPARATION_FORM_CHOISES, max_length=200,
										  default=INCORPARATION_FORM_CHOISES[0], null = True)  # организационно правовая форма
	approver = models.ForeignKey(
		Approver,
		on_delete=models.CASCADE,
		null = True
	)
	obligations = models.CharField(max_length=1000, default='Должностные обязанности', null = True)  # должностные обязаности


class ManyValue(models.Model):  # сделать такую форму, которая будет суммироваться в другие поля
	amount = models.CharField(max_length=15, default="1000", blank=True, null = True)
	currency = models.CharField(max_length=20, choices=CURRANCY_CHOISES, default=CURRANCY_CHOISES[0], null = True)
# class MonthPayValue(models.Model):  # сделать такую форму, которая будет суммироваться в другие поля
# 	amount = models.CharField(max_length=15, default="1000", blank=True)
# 	currency = models.CharField(max_length=20, choices=CURRANCY_CHOISES, default=CURRANCY_CHOISES[0])
# class LeftoverValue(models.Model):  # сделать такую форму, которая будет суммироваться в другие поля
# 	amount = models.CharField(max_length=15, default="1000", blank=True)
# 	currency = models.CharField(max_length=20, choices=CURRANCY_CHOISES, default=CURRANCY_CHOISES[0])

class ClientCredit(models.Model):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE,
		primary_key=False, null = True
	)
	requested_field = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									   default=YES_NO_CHOISES[1], null = True)  # запрашиваемый или в наличии
	type = models.CharField(choices=СREDIT_TYPES, max_length=50, default=СREDIT_TYPES[1], null = True)
	credit_goal = models.CharField(max_length=100, default="Приобретение жилья", blank=True, null = True)  # цель кредита
	special_programms = models.CharField(max_length=100, default="", blank=True, null = True)  # специальные программы
	desired_pay_period = models.CharField(max_length=100, default="2 года", blank=True, null = True)  # желаемый платежный период
	insurance = models.CharField(max_length=100, default="полный пакет", blank=True, null = True)  # страхование рисков
	creditor_name = models.CharField(max_length=100, default="Сбербанк", blank=True, null = True)  #
	#todo сделать виджет количество лет количество месяцев
	duration = models.CharField(max_length=3, default="12", blank=True, null = True)  #Желаемый срок кредитования
	date_start = models.DateField(default="2000-01-01", null = True)
	date_end = models.DateField(default="2005-01-01", null = True)
	value = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		related_name = 'value_rn',
		primary_key=False, null = True
	)  # сумма кредита
	month_pay = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		related_name = 'month_pay_rn',
		primary_key=False, null = True
	)  # месячный платеж
	leftover = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		related_name = 'leftover_rn',
		primary_key=False, null = True
	)  # остаток
	reask = models.CharField(choices=IPOTEKA_REASK, max_length=50, default=IPOTEKA_REASK[0], null = True)

class Ipoteka(ClientCredit):
	property_value = models.CharField(max_length=100, default="1 000 000", blank=True, null = True)  # стоимость объекта недвижимости
	immovables_region = models.CharField(max_length=100, default="Самарский регион",
										 blank=True, null = True)  # регион объекта недвижимости
	immovables_type = models.CharField(choices=IMMOVABLE_PROPERTY_CHOISES, max_length=50,
									   default=IMMOVABLE_PROPERTY_CHOISES[0], null = True)  # регион объекта недвижимости
	product_type = models.CharField(choices=IPOTEKA_TYPES, max_length=50,
									default=IPOTEKA_TYPES[0], null = True)  # наименование ипотечного продукта
	first_pay = models.CharField(max_length=100, default="1000", blank=True, null = True)  # размер первого платежа
	source_for_first_pay = models.CharField(max_length=100, default="личные накопления",
											blank=True, null = True)  # источник первоначального взноса


# дом рф
# наименование опции
# источник информации об ипотечном продукте
class Own(models.Model):
	value = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		primary_key=False, null = True
	)  # стоимость

class Auto(Own):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE, null = True
	)
	car_mark = models.CharField(max_length=100, default="Лада", null = True)
	car_model = models.CharField(max_length=100, default="Лада", null = True)
	year_of_manufacture_of_car = models.CharField(max_length=200, default="год выпуска авто", null = True)


class ImmovableProp(Own):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE, null = True
	)
	address = models.ForeignKey(
		Address,
		on_delete=models.CASCADE, null = True
	)
	type = models.CharField(choices=IMMOVABLE_PROPERTY_CHOISES, max_length=50, default=IMMOVABLE_PROPERTY_CHOISES[0], null = True)
	own_percent = models.CharField(max_length=3, default="100", blank=True, null = True)  # доля в собственности
	square = models.CharField(max_length=100, default="100 m2", blank=True, null = True)  # площадь

###Доход от сдачи в аренду недвижимости может быть несколько объектов
class RentalIncome(models.Model):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE, null = True
	)
	address = models.ForeignKey(
		Address,
		on_delete=models.CASCADE, null = True
	)
	contract_start = models.DateField(default="1999-01-01", null = True)
	contract_end = models.DateField(default="1999-01-01", null = True)
	property_type = models.CharField(choices=IMMOVABLE_PROPERTY_CHOISES, max_length=50,
									 default=IMMOVABLE_PROPERTY_CHOISES[0], null = True)
	count_room = models.CharField(max_length=3, default="2", blank=True, null = True)
	square = models.CharField(max_length=20, default="100", blank=True, null = True)  # m2
	own_percent = models.CharField(max_length=3, default="100", blank=True, null = True)  # доля в собственности
	value = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		primary_key=False, null = True
	)


class PensionValue(models.Model):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE, null = True
	)
	value = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		primary_key=False, null = True
	)

class ClientRelative(Approver):
	client = models.ForeignKey(
		Client,
		on_delete=models.CASCADE,
		primary_key=False, null = True
	)
	relation_degree = models.CharField(choices=RELATION_DEGREE_CHOISES, max_length=300, default=RELATION_DEGREE_CHOISES[0], null = True)
	birthday = models.DateField(default="1999-01-01", null = True)

class AdditionalClientInfo(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True
	)
	home_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # домашний телефон
	сont_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # контактный телефон
	work_phone_number = models.CharField(max_length=12, default='89276976453', null = True)  # рабочий телефон
	email_v = models.CharField(max_length=300, default='', null = True)  # должность
	snils_number = models.CharField(max_length=20, default="123-123-123 00", blank=True, null = True)

	# 	count_of_children = models.CharField(max_length=2, default="0")  # количество детей
	# 	class Meta:
	family_status = models.CharField(choices=FAMILY_STATUS_CHOISES, max_length=13, default=FAMILY_STATUS_CHOISES[0], null = True)
	education_status = models.CharField(choices=EDUCATION_STATUS_CHOISES, max_length=50,
										default=EDUCATION_STATUS_CHOISES[0], null = True)

	marriage_contract = models.CharField(choices=YES_NO_CHOISES, max_length=50,
										 default=YES_NO_CHOISES[0], null = True)  # наличие брачного договора
	rezident_of_usa = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									   default=YES_NO_CHOISES[0], null = True)  # Являетесь ли вы налоговым резидентом США
	rezident_of_other_goverment = models.CharField(choices=YES_NO_CHOISES, max_length=50,
												   default=YES_NO_CHOISES[0], null = True)  # Являетесь ли вы налоговым резидентом другого государства за исключением США
	foreign_citizen = models.CharField(choices=YES_NO_CHOISES, max_length=50,
									   default=YES_NO_CHOISES[0], null = True)  # Являетесь ли вы иностранным гражданином
	reason_for_secondFIO = models.CharField(max_length=30, default='Вышла замуж', null = True)
	second_first_name = models.CharField(max_length=30, default='Иван', null = True)
	second_part_name = models.CharField(max_length=30, default='Иванович', null = True)
	second_last_name = models.CharField(max_length=30, default='Иванов', null = True)
	work_experiance_general = models.CharField(max_length=10, default='10', null = True) #Общий стаж работы
	work_experiance_by_profile = models.CharField(max_length=3, default='10', null = True) #Стаж работы по профилю
	role = models.CharField(choices=CLIENT_ROLE, max_length=3, default='10', null = True) #Роль в сделке
	relation_degree = models.CharField(choices=CLIENT_ROLE, max_length=3, default=CLIENT_ROLE[0], null = True) #Степень родства с заемщиком
	was_bankrot = models.CharField(choices=YES_NO_CHOISES, max_length=3, default=YES_NO_CHOISES[0], null = True) #Применялась ли процедура банкротства
	aliments = models.ForeignKey(
		ManyValue,
		on_delete=models.CASCADE,
		primary_key=False,
		null = True,
		blank = True
	) #Алименты
	# aliments = models.CharField(max_length=10, default='10') #Планируете ли вы покупать жилье по программе жилье для российской семьи
	exist_zg_passport = models.CharField(choices=YES_NO_CHOISES, max_length=3, default=YES_NO_CHOISES[0], null = True) #Есть ли загран паспорт
