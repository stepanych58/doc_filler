from django import forms
from django.forms import CheckboxInput, NumberInput, DateInput
from .models import *


class UploadTemplateForm(forms.Form):
    #title = forms.CharField(max_length=50, label = 'Template Name')
    template = forms.FileField(label = 'Choose template');

class StbeField(forms.Widget):
    label_value ='stbe1234545566'
    template_name = 'label.html'
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label_value'] = self.label_value
        return context


class ClientForm(forms.ModelForm):
     class Meta:
         model = Client
         fields = ['first_name', 'part_name', 'last_name',]

class ClientChecked(forms.Form):
    cl_check = forms.CharField(widget=CheckboxInput(), label = 'ch_l',required=False)

class UserlistForm(forms.Form):
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")

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
        labels ={'number':'Номер (№)',}
        fields =['number',]
# '''
# 		'документ':'пасспорт гр. РФ',
# 		'серия': '3345',
# 		'номер': '180009',
# 		'Пасспорт выдан':'ОТДЕЛОМ УФМС РОССИИ ПО САМАРСКОЙ ОБЛАСТИ В ГОРОДЕ МАХАЧКАЛА',
# 		'Фамилия':'Берендяев',
# 		'Имя':'Степан',
# 		'Отчество':'Владимирович',
# 		'пол':'муж.',
# 		'Дата рождения':'23.07.1999',
# 		'Место рождения':'г. Саратов Самарская обл.'
# '''

