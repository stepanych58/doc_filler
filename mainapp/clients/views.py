import json
import os

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import render
from doc_filler_app.main_file_filler import *
from mainapp.settings import *

from .forms import *
from .utils import *

DELETE = 'Delete'
GENERATE = 'Generete Doc'
DELETE_GEN_DOC = 'Delete generated doc'

view_params = {'all_clients': Client.objects.all(),
			   'page_title': 'Clients page',
			   'all_docs': Document.objects.all(),
			   'test_param': 'tp',
			   'p_table': 'clients',
			   'all_clients_files': ClientsFile.objects.all(), }


def welcomePage(request):
	username = auth.get_user(request).username
	context = {'username': username}
	return render(request, 'welcome.html', context)


@login_required()
def allClients(request, test_param="tp"):
	username = auth.get_user(request).username
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	view_params['p_table'] = 'clients'
	view_params['page_title'] = 'Клиенты'
	view_params['username'] = username
	return render(request, 'index.html', view_params);


@login_required
def allTemplates(request):
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	view_params['p_table'] = 'templates'
	view_params['page_title'] = 'Анкеты'
	return render(request, 'index.html', view_params);


@login_required
def addClient(request):
	post = request.POST
	sbm = post['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),
												  'client_f': ClientForm(),
												  'passport_f': PassportForm(),
												  'registration_addr_f': AddressForm(),
												  'job_addr_f': AddressForm(),
												  'job_f': JobInfoForm(),
												  'bankdetail_f': BankDetailForm(),
												  'approver_f': ApproverForm(),
												  'credit_f': IpotekaForm(),
												  'relative_f': ClientRelativeForm(),
												  'rental_f': RentalIncomeForm(),
												  'pension_f': PensionValueForm(),
												  # 's_f': StbeTestForm(),
												  # 'credit_f': credits_factory,
												  # 'client_f': client_form_set,
												  # 'address_f': address_factory,
												  # 'postaddress_f': post_address_factory,
												  # 'bankdetail_f': bank_detail_factory,
												  # 'orginfo_f': organization_factory,
												  'additional_client_info_f': AdditionalClientInfoForm(),
												  })
	elif sbm == 'Add':
		client = ClientForm(post);
		client.save()
	# snils = snils_factory(post)
	# address = address_factory(post)
	# post_address = post_address_factory(post)
	# organization = organization_factory(post)
	# bank_detail = bank_detail_factory(post)
	# additional_client_info = additional_client_info_factory(post)
	# credit = credits_factory(post)
	#
	# if (client.is_valid() and passport.is_valid() and address.is_valid() and bank_detail.is_valid() and
	# 		snils.is_valid() and organization.is_valid() and post_address.is_valid()):
	# 	client = client.save()
	# 	passport.instance.client = client
	# 	passport.save()
	# 	snils.instance.client = client
	# 	todo dont add existing addresses in table
	# 	address = address.save()
	# 	post_address = post_address.save()
	# 	bank_detail = bank_detail.save()
	# 	organization.instance.client = client
	# 	organization.instance.address = address
	# 	organization.instance.bank_detail = bank_detail
	# 	organization.instance.post_address = post_address
	# 	organization.save()
	# 	additional_client_info.instance.client = client
	# 	credit.instance.client = client
	# 	additional_client_info.save()
	# 	credit.save()
	# if additional_client_info.is_valid():
	# 	additional_client_info.save()
	# else:
	# 	print(additional_client_info.errors)
	# else:
	# 	for errorform in (
	# 			client, passport, snils, address, bank_detail, organization, additional_client_info,
	# 			credit):
	# 		print(errorform.errors)
	return HttpResponseRedirect('/clients/');


def deleteClient(client_ids):
	clients = Client.objects.filter(id__in=client_ids)
	clients.delete();


@login_required
def deleteTemplate(template_id):
	Document.objects.get(id=template_id).delete();


@login_required
def deleteGenDoc(gen_doc_id):
	ClientsFile.objects.get(id=gen_doc_id).delete();


def clientForm(request):
	print('clientForm start')
	btn = request.POST.get('sbm')
	page = request.POST.get('page')
	doc_id = request.POST.get('doc_id')
	gen_doc_id = request.POST.get('clientf_id')
	che = request.POST.getlist('cl_checked')
	if (
			btn == None and
			page == None and
			doc_id == None and
			gen_doc_id == None
	):
		return HttpResponseRedirect('/clients/')
	if btn == DELETE:
		deleteClient(che)
	if btn == DELETE and page == 'templates':
		deleteTemplate(client_id)
	if btn == DELETE_GEN_DOC:
		deleteGenDoc(gen_doc_id)
	return HttpResponseRedirect('/clients/');


@login_required
def createTestData(request):
	create_test_data()
	return HttpResponseRedirect('/clients/');


@login_required
def clearData(request):
	Client.objects.all().delete()
	Document.objects.all().delete()
	return HttpResponseRedirect('/clients/');


@login_required
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


@login_required
def generateReport(request):
	print(request)
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	clientids = json_view_params['checkedClients']
	pdocs = json_view_params['checkedDocs']
	for client_id in clientids:
		writeClientDoc(client_id, pdocs[0])
	return HttpResponseRedirect('/clients/');


@login_required
def addTemplate(request):
	return render(request, 'addTemplate.html', {'doc_f': modelformset_factory(Client, fields='__all__')})


def login(request):
	return render(request, 'accounts/login.html')
