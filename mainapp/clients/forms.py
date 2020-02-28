from django import forms
from django.forms.widgets import Input, Select, DateInput, Textarea, EmailInput, NumberInput
from clients.choises import *
from clients.models import *


# Util methods
from clients.widgets import ManyValueInput


def aplyForAll(field, widget):
	resultDict = {}
	for i in field:
		resultDict[i] = widget
	return resultDict;


def printCol(self,
			 div1_class='col-md-5',
			 label_id='', label='', input='',
			 inputName='', inputValue='', inputId='' ):
	attrs = {'id' : 'id_' + str(inputId)};
	if isinstance(input, Select):
		if input.attrs.get('choices', None) == 'small1':
			div1_class='col-md-1'
		elif input.attrs.get('choices', None) == 'small2':
			div1_class='col-md-2'
	return '<div class="' + div1_class + '">' + \
		   '<label for="id_' + label_id + '">' + label + '</label>' + \
		   input.render(name=inputName, value=inputValue , attrs =attrs) + \
		   '</div>' + \
		   '<div class="invalid-feedback">' + \
		   'Valid '+ label + ' is required.' + \
		   '</div>';


simpleInput = Input(attrs={'class': 'form-control', })
simpleDate = DateInput(attrs={'class': 'form-control', 'type': 'date'})

class AbstractForm(forms.ModelForm):
	def printForm(self):
		resStr = '<div class="row">'
		for label in self.Meta.widgets:
			resStr += printCol(self, label_id=label, div1_class='col-md-4 mb-3', inputName = label,
							   label=self.Meta.labels[label],
							   input=self.Meta.widgets[label], inputId=label)
		resStr += '</div>'
		return resStr;


class ClientForm(AbstractForm):
	class Meta:
		model = Client
		fields = '__all__'
		labels = {'last_name': 'Фамилия',
				  'first_name': 'Имя',
				  'part_name': 'Отчество', }
		widgets = aplyForAll(labels.keys(), simpleInput)

class AddressForm(AbstractForm):
	class Meta:
		model = Address
		exclude = ('client',)
		labels = {
			'index': 'Индекс',
			'country': 'Страна',
			'city': 'Город',
			'street': 'Улица',
			'buildingNumber': 'Номер дома',
			'housing': 'Корпус',
			'structure': 'Строение',
			'flat': 'Квартира',
			'oblast': 'Область',
			'rayon': 'Район',
		}
		widgets = aplyForAll(labels.keys(), simpleInput)

class PassportForm(forms.ModelForm):
	class Meta:
		model = Passport
		fields = ['serial', 'number', 'v_from', 'date_of', 'gender', 'birthday', 'code_of', ]
		labels = {'serial': 'Серия',
				  'number': 'Номер',
				  'v_from': 'Кем выдан',
				  'gender': 'пол',
				  'birthday': 'Дата рождения',
				  'date_of': 'Дата выдачи',
				  'code_of': 'Код подразделения',
				  }
		widgets = {
			'serial': simpleInput,
			'number': simpleInput,
			'v_from': Textarea(attrs={'class': 'form-control', 'style': 'height: 95px;'}),
			'gender': Select(attrs={'class': 'form-control', 'choices':'small1'}, choices=GENDER_CHOISES),
			'birthday': simpleDate,
			'date_of': simpleDate,
			'code_of': simpleInput,
		}

	def printForm(self):
		resStr = '<div class="row">'
		v_fromLabel = self.Meta.fields[2]
		for label in self.Meta.fields[:2]:
			resStr += printCol(self, label_id=label, div1_class='col-md-4 mb-3', inputName = label,
							   label=self.Meta.labels[label],
							   input=self.Meta.widgets[label], inputId=label)
		resStr += '</div>'
		resStr += '<div class="row">'
		resStr += printCol(self, label_id=v_fromLabel, div1_class='col-md-8', inputName=v_fromLabel,
				 label=self.Meta.labels[v_fromLabel],
				 input=self.Meta.widgets[v_fromLabel], inputId=v_fromLabel)
		resStr += '</div>'
		resStr += '<div class="row">'
		for label in self.Meta.fields[3:7]:
			resStr += printCol(self, label_id=label, div1_class='col-md-3 mb-3', inputName = label,
							   label=self.Meta.labels[label],
							   input=self.Meta.widgets[label], inputId=label)
		resStr += '</div>'
		return resStr;

class ApproverForm(ClientForm):
	class Meta:
		model = Approver
		fields = '__all__'
		labels = {'last_name': 'Фамилия',
				  'first_name': 'Имя',
				  'part_name': 'Отчество',
				  'position': 'Должность',
				  'phone_number': 'Телефонный номер',
				  'email_v': 'Email', }
		widgets = aplyForAll(labels.keys(), simpleInput)

class JobInfoForm(AbstractForm):
	class Meta:
		model = JobInfo
		exclude = ('client', 'address', 'bank_detail', 'approver')
		labels = {
			'is_general': 'Основное место работы',
			'full_name': 'Полное наименование организации',
			'inn_number': 'ИНН',
			'account_phone_number': 'Телефон бугалтерии',
			'hr_phone_number': 'Телефон отдела кадров',
			'work_phone_number': 'Рабочий телефон',
			'age': 'Возраст организации',
			'number_of_staff': 'Количество сотрудников',
			'work_experience': 'Cтаж в данной организации',
			'site': 'Cайт организации',
			'position': 'Должность',
			'position_category': 'Категория должности',
			'salary': 'Доход до налогооблажения',
			'is_probation': 'Испытательный срок',
			'kind_of_contract': 'Вид договора',  # (Понайму, бессрочный, по найму срочный)
			'contract_start': 'Дата заключения договора',
			'contract_end': 'Дата окончания договора',
			'incorparation_form': 'Организационно правовая форма',
			'obligations': 'Должностные обязанности',
		}
		textFields = ('site', 'age', 'position',
					  'salary', 'obligations', 'full_name', 'inn_number',
					  'account_phone_number', 'hr_phone_number', 'work_phone_number',)
		selectwidgets = {
			'is_general': Select(attrs={'class': 'form-control', }, choices=YES_NO_CHOISES),
			'is_probation': Select(attrs={'class': 'form-control', }, choices=YES_NO_CHOISES),
			'incorparation_form': Select(attrs={'class': 'form-control', }, choices=INCORPARATION_FORM_CHOISES),
			'kind_of_contract': Select(attrs={'class': 'form-control', }, choices=KINDS_OF_CONTRACT),
			# (Понайму, бессрочный, по найму срочный)
			'position_category': Select(attrs={'class': 'form-control', }, choices=POSITION_CATEGORY_CHOISES),
			'number_of_staff': Select(attrs={'class': 'form-control', }, choices=NUMBER_OF_STAFF_CHOISES),
			'work_experience': Select(attrs={'class': 'form-control', }, choices=WORK_EXPERIENCE_CHOISES),
		}
		dateWidgets = {
			'contract_start': simpleDate,
			'contract_end': simpleDate,
		}
		allWidgets = {}
		allWidgets.update(aplyForAll(textFields, widget=simpleInput))
		allWidgets.update(selectwidgets)
		allWidgets.update(dateWidgets)
		widgets = allWidgets

class BankDetailForm(AbstractForm):
	class Meta:
		model = BankDetail
		fields = '__all__'
		labels = {
			'account_number': 'Номер рассчетного счета',
			'correspondent_account_number': 'Номер корреспондентского счета',
			'bic': 'BIC',
			'bank_name': 'Имя банка'
		}
		widgets = aplyForAll(labels.keys(), simpleInput)

class AdditionalClientInfoForm(AbstractForm):
	class Meta:
		model = AdditionalClientInfo
		fields = ['snils_number']
		labels = {'snils_number': 'СНИЛС', }
		widgets = {'snils_number': simpleInput}

class CreditForm(AbstractForm):
	class Meta:
		model = ClientCredit
		exclude = ('client',)
		labels = {
			'requested_field': 'Запрашиваемый?',
			'type': 'Тип кредита',
			'credit_goal': 'Цель кредита',
			'special_programms': 'Специальные программы',
			'desired_pay_period': 'Желаемый платежный период',
			'insurance': 'Страхование рисков',
			'creditor_name': 'Банк кредитор',
			'date_start': 'Дата начала кредитования',
			'date_end': 'Дата окончания кредита',
			'value': 'Cумма кредита',
			'month_pay': 'Месячный платеж',
			'leftover': 'Остаток'}
		widgets = {
			'requested_field': Select(attrs={'class': 'form-control', 'choices':'small2'}, choices=YES_NO_CHOISES),
			'type': Select(attrs={'class': 'form-control', }, choices=СREDIT_TYPES),
			'credit_goal': simpleInput,
			'special_programms': simpleInput,
			'desired_pay_period': simpleInput,
			'insurance': simpleInput,
			'creditor_name': simpleInput,
			'date_start': simpleDate,
			'date_end': simpleDate,
			'value': ManyValueInput(),
			'month_pay': ManyValueInput(),
			'leftover': ManyValueInput(),
		}


class IpotekaForm(CreditForm):
	class Meta:
		model = Ipoteka
		fields = '__all__'


class ClientRelativeForm(ApproverForm):
	class Meta:
		model = ClientRelative
		exclude = ('client',)
		labels = {'last_name': 'Фамилия',
				  'first_name': 'Имя',
				  'part_name': 'Отчество',
				  'position': 'Должность',
				  'phone_number': 'Телефонный номер',
				  'email_v': 'Email', }
		widgets = {
			'last_name': simpleInput,
			'part_name': simpleInput,
			'position': simpleInput,
			'phone_number': simpleInput,
			'email_v': EmailInput(attrs={'class': 'form-control', }),
			'first_name': Input(attrs={
				'class': 'form-control',
				'type': 'text',
				'placeholder': '',
			}),
		}
