from django import forms
from .models import *


class UploadTemplateForm(forms.Form):
    #title = forms.CharField(max_length=50, label = 'Template Name')
    template = forms.FileField(label = 'Choose template');


class ClientForm(forms.ModelForm):
     class Meta:
         model = Client
         fields = ['first_name', 'part_name', 'last_name',]

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

class OrganizationInfoForm(forms.ModelForm):
    class Meta:
        model = OrganizationInfo
        fields = [
            'full_name',
            'client',
        ]