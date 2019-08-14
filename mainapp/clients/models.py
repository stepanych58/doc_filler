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
	# class Meta:
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