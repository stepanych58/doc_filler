import json
import os

from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory, modelform_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from doc_filler_app.main_file_filler import *
from mainapp.settings import *

from .forms import *
from .utils import *

# ALL_CLIENTS = Client.objects.all()
# ALL_DOCS = Document.objects.all()

DELETE = 'Delete'
GENERATE = 'Generete Doc'
DELETE_GEN_DOC = 'Delete generated doc'

view_params = {'all_clients': Client.objects.all(),
			   'page_title': 'Clients page',
			   'all_docs': Document.objects.all(),
			   'test_param': 'tp',
			   'p_table': 'clients',
			   'all_clients_files': ClientsFile.objects.all(), }

client_form_set = modelform_factory(Client, fields='__all__',
									labels={'last_name': 'Фамилия',
											'first_name': 'Имя',
											'part_name': 'Отчество',
											'position': 'Должность',
											'phone_number': 'Телефонный номер',
											'email': 'Email', })
passport_factory = modelform_factory(Passport, fields=['serial', 'number', '_from', 'date_of', 'gender', 'birthday',
													   'code_of', ],
									 labels={'serial': 'Серия',
											 'number': 'Номер',
											 '_from': 'Кем выдан',
											 'gender': 'пол',
											 'birthday': 'Дата рождения',
											 'date_of': 'Дата выдачи',
											 'code_of': 'Код подразделения',
											 }
									 )
snils_factory = modelform_factory(SNILS, fields=['snils_number'], labels={'snils_number': 'Номер №'})
address_factory = modelform_factory(Address, fields=['index',
													 'city',
													 'street',
													 'buildingNumber',
													 'housing',
													 'structure',
													 'flat',
													 'oblast',
													 'rayon', ],
									labels={
										'index': 'Индекс',
										'city': 'Город',
										'street': 'Улица',
										'buildingNumber': 'номер дома',
										'housing': 'корпус',
										'structure': 'строение',
										'flat': 'квартира',
										'oblast': 'Область',
										'rayon': 'район',
									}
									)
post_address_factory = modelform_factory(PostAddress, fields=['index',
															  'city',
															  'street',
															  'buildingNumber',
															  'housing',
															  'structure',
															  'flat',
															  'oblast',
															  'rayon', ],
										 labels={
											 'index': 'Индекс',
											 'city': 'Город',
											 'street': 'Улица',
											 'buildingNumber': 'номер дома',
											 'housing': 'корпус',
											 'structure': 'строение',
											 'flat': 'квартира',
											 'oblast': 'Область',
											 'rayon': 'район',
										 })
bank_detail_factory = modelform_factory(BankDetail, fields=['account_number',
															'correspondent_account_number',
															'bic',
															'bank_name', ],
										labels={
											'account_number': 'Номер счета',
											'correspondent_account_number': 'Номер Корреспондентского счета',
											'bic': 'БИК',
											'bank_name': 'Название банка',
										})
organization_factory = modelform_factory(OrganizationInfo, fields=['full_name',
																   'accountent_number',
																   'hr_number',
																   'inn_number',
																   'field_of_activity',
																   'incorparation_form',
																   'number_of_staff',
																   'work_experience', ],
										 labels={'full_name': 'Полное имя организации',
												 'accountent_number': 'Номер счета',
												 'hr_number': 'Номер отдела кадров',
												 'inn_number': 'ИНН',
												 'field_of_activity': 'Должность',
												 'incorparation_form': 'Сфера деятельности организации',
												 'number_of_staff': 'Количество сотрудников',
												 'work_experience': 'Опыт работы', }
										 )
additional_client_info_factory = modelform_factory(AdditionalClientInfo, fields=['product',
																				 'property',
																				 'full_insurance',
																				 'registration',
																				 'address_of_registration',
																				 'actual_address',
																				 'count_of_children',
																				 'family_status',
																				 'education_status',
																				 'work_expireance',
																				 'position_category',
																				 'work_type',
																				 'marriage_contract',
																				 'immovable_property',
																				 'rezident_of_usa',
																				 'rezident_of_other_goverment',
																				 'foreign_citizen',
																				 'additional_work',
																				 'additional_work_expireance',
																				 'additional_work_category',
																				 'income_of_main_work',
																				 'income_of_additional_work',
																				 'mark_of_car',
																				 'year_of_manufacture_of_car',
																				 'car_valuation',
																				 'car_valuation',
																				 'market_value_of_real_estate', ],
												   labels={'product': 'Тип кредита',
														   'property': 'Тип имущества',
														   'full_insurance': 'Полное страхование',
														   'registration': 'Регистрация',
														   'address_of_registration': 'Адрес фактического проживания',
														   'actual_address': 'Адрес проживания',
														   'count_of_children': 'Кол-во детей',
														   'family_status': 'Семейное положение',
														   'education_status': 'образование',
														   'work_expireance': 'Стаж работы на текущем месте работы',
														   'position_category': 'Категория должности',
														   'work_type': 'Тип занятости',
														   'marriage_contract': 'Наличие брачного договора',
														   'immovable_property': 'Неджимиое имущество в собственности',
														   'rezident_of_usa': 'Являетесь ли вы налоговым резидентом США',
														   'rezident_of_other_goverment': 'Являетесь ли вы налоговым резидентом другого государства за исключением США',
														   'foreign_citizen': 'Является ли клиент иностранным гражданином',
														   'additional_work': 'Работа по совместительству',
														   'additional_work_expireance': 'Стаж работы по совместительству',
														   'additional_work_category': 'Категория должности работы по совместительству',
														   'income_of_main_work': 'Доход от основной деятельности',
														   'income_of_additional_work': 'Доход от работы по совместительству',
														   'mark_of_car': 'марка автомобиля',
														   'year_of_manufacture_of_car': 'год выпуска автомобиля',
														   'car_valuation': 'оценка стоимости автомобиля',
														   'market_value_of_real_estate': 'Рыночная стоимость недвижимости',
														   })


def welcomePage(request):
	return render(request, 'welcome.html')


def allClients(request, test_param="tp"):
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	view_params['p_table'] = 'clients'
	view_params['page_title'] = 'Clients page'
	return render(request, 'index.html', view_params);


def allTemplates(request):
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	view_params['p_table'] = 'templates'
	view_params['page_title'] = 'Templates page'
	return render(request, 'index.html', view_params);


def addClient(request):
	post = request.POST
	sbm = post['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),
												  'passport_f': passport_factory,
												  'snils_f': snils_factory,
												  'client_f': client_form_set,
												  'address_f': address_factory,
												  'postaddress_f': post_address_factory,
												  'bankdetail_f': bank_detail_factory,
												  'orginfo_f': organization_factory,
												  'additional_client_info_f': additional_client_info_factory,
												  })
	elif sbm == 'Add':
		client = client_form_set(post)
		passport = passport_factory(post)
		snils = snils_factory(post)
		address = address_factory(post)
		post_address = post_address_factory(post)
		organization = organization_factory(post)
		bank_detail = bank_detail_factory(post)
		additional_client_info = additional_client_info_factory(post)

		if (client.is_valid() and passport.is_valid() and address.is_valid() and bank_detail.is_valid() and
				snils.is_valid() and organization.is_valid() and post_address.is_valid()):
			client = client.save()
			passport.instance.client = client
			passport.save()
			snils.instance.client = client
			# todo dont add existing addresses in table
			address = address.save()
			post_address = post_address.save()
			bank_detail = bank_detail.save()
			organization.instance.client = client
			organization.instance.address = address
			organization.instance.bank_detail = bank_detail
			organization.instance.post_address = post_address
			organization.save()
			additional_client_info.instance.client = client
			additional_client_info.save()
		else:
			for errorform in (
					client, passport, snils, address, bank_detail, organization, post_address, additional_client_info):
				print(errorform.errors)
	return HttpResponseRedirect('/clients/');


def clientInfo(request, client_id):
	client = Client.objects.get(id=client_id)
	return render(request, 'client.html', {'resulthtml': ClientHTML.printHTML(client), })


def deleteClient(client_id):
	client = Client.objects.get(id=client_id)
	client.delete();


def deleteTemplate(template_id):
	Document.objects.get(id=template_id).delete();


def deleteGenDoc(gen_doc_id):
	ClientsFile.objects.get(id=gen_doc_id).delete();


def clientForm(request, client_id):
	btn = request.POST.get('sbm')
	page = request.POST.get('page')
	doc_id = request.POST.get('doc_id')
	gen_doc_id = request.POST.get('clientf_id')
	if (
			btn == None and
			page == None and
			doc_id == None and
			gen_doc_id == None
	):
		return HttpResponseRedirect('/clients/')
	if btn == DELETE and page == 'clients':
		deleteClient(client_id)
	if btn == DELETE and page == 'templates':
		deleteTemplate(client_id)
	if btn == DELETE_GEN_DOC:
		deleteGenDoc(gen_doc_id)
	return HttpResponseRedirect('/clients/');


def createTestData(request):
	create_test_data()
	return HttpResponseRedirect('/clients/');


def clearData(request):
	Client.objects.all().delete()
	Document.objects.all().delete()
	return HttpResponseRedirect('/clients/');


def uploadTemplate(request):
	# add logic to save template in certain directory https://www.programcreek.com/python/example/59557/django.core.files.storage.FileSystemStorage
	if request.method == 'POST':
		uploaded_file = request.FILES['template']
		tmp_name = request.POST['tmp_name']
		file_name = os.path.splitext(uploaded_file.name)[0]
		ext = os.path.splitext(uploaded_file.name)[1]
		file_name += ext
		loc, type = None, None
		if ext == PDF_EXT:
			loc, type, res_mes = PDF_TEMPL_DIR, PDF, 'PDF File uploaded';
		elif ext == DOC_EXT:
			loc, type, res_mes = DOC_TEMPL_DIR, DOC, 'DOC File uploaded';
		elif ext == TXT_EXT:
			loc, type, res_mes = TXT_TEMPL_DIR, TXT, 'TXT File uploaded';
		elif ext == EXEL_EXT:
			loc, type, res_mes = EXEL_TEMPL_DIR, EXEL, 'Exel File uploaded';
		else:
			view_params['test_param'] = 'No file extentions!'
			return HttpResponseRedirect('/clients/');
		view_params['test_param'] = res_mes
		FileSystemStorage(location=loc).save(file_name, uploaded_file)
		Document(name=tmp_name, file_name=file_name, file_type=type).save()
	return HttpResponseRedirect('/clients/');


def testPage(request):
	if request.method == 'POST':
		client = ClientForm(request.POST)
		client.save()
	else:
		clientForm = ClientForm()
	return render(request, 'test_page.html', {'client_form': modelformset_factory(Client, fields='__all__'),
											  'page_text_param': '', })


def generateReport(request):
	print(request)
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	clientids = json_view_params['checkedClients']
	pdocs = json_view_params['checkedDocs']
	for client_id in clientids:
		writeClientDoc(client_id, pdocs[0])
	return HttpResponseRedirect('/clients/');


def addTemplate(request):
	return render(request, 'addTemplate.html', {'doc_f': modelformset_factory(Client, fields='__all__')})
