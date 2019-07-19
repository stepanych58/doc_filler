from django.db import models

class Client(models.Model):
	first_name = models.CharField(max_length=30)
	part_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)

class Document(models.Model):
	name = models.CharField(max_length=500)

# Create your models here.
