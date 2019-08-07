from django import forms
from .models import *


class UploadTemplateForm(forms.Form):
    #title = forms.CharField(max_length=50, label = 'Template Name')
    template = forms.FileField(label = 'Choose template');

#todo try to use inlineformset_factory instead form class for each object type
class ClientForm(forms.ModelForm):
     class Meta:
         model = Client
         labels = {
             'last_name': 'Фамилия',
             'first_name':'Имя',
             'part_name':'Отчество',
             'position':'Должность',
         }
         fields = [
             'last_name',
             'first_name',
             'part_name',
             'position',
         ]

class PassportForm(forms.ModelForm):
    class Meta:
        model = Passport
        labels = {
            'serial': 'Серия',
            'number': 'Номер',
            '_from': 'Кем выдан',
            'gender': 'пол',
            'bith_day': 'Дата рождения',
            'bith_place': 'Место рождения',
        }
        fields = ['serial',
                  'number',
                  '_from',
                  'gender',
                  'bith_day',
                  'bith_place',
                  ]

class SNILSForm(forms.ModelForm):
    class Meta:
        model = SNILS
        labels ={'snils_number':'Номер (№)',}
        fields =['snils_number',]

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        labels = {
            'index':'Индекс',
            'city':'Город/Населенный пункт',
            'street':'Улица',
            'buildingNumber':'Номер дома',
            'housing':'Корпус',
            'structure':'Строение',
            'flat':'Офис/Квартира',
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
            'index':'Индекс',
            'city':'Город/Населенный пункт',
            'street':'Улица',
            'buildingNumber':'Номер дома',
            'housing':'Корпус',
            'structure':'Строение',
            'flat':'Офис/Квартира',
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
            'account_number':'Номер рассчетного счета',
            'correspondent_account_number':'Номер корреспондентского счета',
            'bic':'БИК',
            'bank_name':'Наименование банка в котором открыт рассчетный счет',
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
        labels ={
            'full_name':'Полное наименование организации работодателя',
            'accountent_number':'Телефон(ы) отдела кадров',
            'hr_number':'Телефон(ы) бухгалтерии',
            'inn_number':'ИНН',
        }
        fields = [
            'full_name',
            'accountent_number',
            'hr_number',
            'inn_number',
        ]
