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
	client = models.ForeignKey(Client, on_delete = models.CASCADE)
	info = jsonfield.JSONField()