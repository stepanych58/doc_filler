from django import forms
from .models import *


class UploadTemplateForm(forms.Form):
	# title = forms.CharField(max_length=50, label = 'Template Name')
	template = forms.FileField(label='Choose template');


class ClientHTML:
    def printField(fied=''):
        #add possible to edit each field
        return fied.__str__()
    def printHTML(self):
        client = Client(self)
        passport = client.passport
        return  \
               '<br>Name: ' + ClientHTML.printField(fied=client.first_name) + ' ' + ClientHTML.printField(client.part_name) + ' ' +  ClientHTML.printField(client.last_name)  + \
               '<br>Position: ' + client.position.__str__() + \
               '<br>Email: ' + client.email.__str__()+\
			   '<br>Passport' ;


class SNILSForm(forms.ModelForm):
	class Meta:
		model = SNILS
		labels = {'snils_number': 'Номер (№)', }
		fields = ['snils_number', ]


class AddressForm(forms.ModelForm):
	class Meta:
		model = Address
		labels = {
			'index': 'Индекс',
			'city': 'Город/Населенный пункт',
			'street': 'Улица',
			'buildingNumber': 'Номер дома',
			'housing': 'Корпус',
			'structure': 'Строение',
			'flat': 'Офис/Квартира',
		}
		fields = [
			'index',
			'city',
			'street',
			'buildingNumber',
			'housing',
			'structure',
			'flat',
		]


class PostAddressForm(forms.ModelForm):
	class Meta:
		model = PostAddress
		labels = {
			'index': 'Индекс',
			'city': 'Город/Населенный пункт',
			'street': 'Улица',
			'buildingNumber': 'Номер дома',
			'housing': 'Корпус',
			'structure': 'Строение',
			'flat': 'Офис/Квартира',
		}
		fields = [
			'index',
			'city',
			'street',
			'buildingNumber',
			'housing',
			'structure',
			'flat',
		]


class BankDetailForm(forms.ModelForm):
	class Meta:
		model = BankDetail
		labels = {
			'account_number': 'Номер рассчетного счета',
			'correspondent_account_number': 'Номер корреспондентского счета',
			'bic': 'БИК',
			'bank_name': 'Наименование банка в котором открыт рассчетный счет',
		}
		fields = [
			'account_number',
			'correspondent_account_number',
			'bic',
			'bank_name',
		]


class OrganizationInfoForm(forms.ModelForm):
	class Meta:
		model = OrganizationInfo
		labels = {
			'full_name': 'Полное наименование организации работодателя',
			'accountent_number': 'Телефон(ы) отдела кадров',
			'hr_number': 'Телефон(ы) бухгалтерии',
			'inn_number': 'ИНН',
		}
		fields = [
			'full_name',
			'accountent_number',
			'hr_number',
			'inn_number',
		]
