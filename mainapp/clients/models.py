# from django.contrib.postgres.fields import JSONField
from django.db import models
from mainapp.settings import *
import jsonfield
#PDF TEMPLATE DIR
PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
#PDF GENERETED RESULT DIR
PDF_GENERATED_RESULT_DIR = STATICFILES_DIRS[3]


class Client(models.Model):
	first_name = models.CharField(max_length=30)
	part_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	class Meta:
		unique_together = ('first_name', 'part_name', 'last_name',)

class Document(models.Model):
	name = models.CharField(max_length=500)
	file_name = models.CharField(max_length=500, default = "file name")
	file_type = models.CharField(max_length=20, default = "pdf")
	
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
	_from = models.CharField(max_length=200, default = "")
	gender = models.CharField(max_length=5, default = "м")
	bith_day = models.DateField(default="1999-01-01")
	bith_place = models.CharField(max_length=200, default = "")

class SNILS(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True,
	)
	number = models.CharField(max_length=20, default="123-123-123 00")

class Address(models.Model):
	index = models.CharField(max_length=6)
	city = models.CharField(max_length=6)
	street = models.CharField(max_length=6)
	buildingNumber = models.CharField(max_length=6)
	housing = models.CharField(max_length=6)
	structure = models.CharField(max_length=6)
	flat = models.CharField(max_length=6)

class BankDetail(models.Model):
	account_number = models.CharField(max_length=20)
	correspondent_account_number =models.CharField(max_length=20)
	BIC = models.CharField(max_length=9)
	bank_name = models.CharField(max_length=1000)
# Bank Account Number: (20 digits)
# Correspondent account number: (20 digits) BIC: (9 digits)
# Name of the bank in which the current account is open:

class OrganizationInfo(models.Model):
	client = models.OneToOneField(
		Client,
		on_delete=models.CASCADE,
		primary_key=True
	)
	full_name = models.CharField(max_length=10000)
	address = models.ForeignKey(
		Address,
		on_delete=models.CASCADE,
	)
	# post_address = models.ForeignKey(
	# 	Address,
	# 	on_delete=models.CASCADE,
	# 	primary_key=True
	# )
	bank_detail = models.ForeignKey(
		BankDetail,
		on_delete=models.CASCADE,
	)
	accountent_number = models.CharField(max_length=10)
	hr_number = models.CharField(max_length=10)
	inn_number = models.CharField(max_length=100)