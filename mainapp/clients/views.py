from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
	return render(request, 'welcome.html',  context)


@login_required()
def allClients(request):
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	view_params['p_table'] = 'clients'
	view_params['username'] = auth.get_user(request).username
	return render(request, 'index.html', view_params);

@login_required
def addClient(request):
	username = auth.get_user(request).username
	post = request.POST
	sbm = post['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),
												  'client_f': ClientForm(),
												  'passport_f': PassportForm(),
												  'registration_addr_f': AddressForm(counter=0),
												  'job_addr_f': AddressForm(counter=2),
												  'job_f': JobInfoForm(),
												  'bankdetail_f': BankDetailForm(),
												  'approver_f': ApproverForm(),
												  'credit_f': IpotekaForm(),
												  'relative_f': ClientRelativeForm(),
												  'rental_f': RentalIncomeForm(),
												  'pension_f': PensionValueForm(),
												  'imm_prop_f': ImmovablePropForm(),
												  'car_f': AutoForm(),
												  'p_table': 'addClient',
												  'username': username,
												  # 's_f': StbeTestForm(),
												  # 'credit_f': credits_factory,
												  # 'client_f': client_form_set,
												  # 'address_f': address_factory,
												  # 'postaddress_f': post_address_factory,
												  # 'bankdetail_f': bank_detail_factory,
												  # 'orginfo_f': organization_factory,
												  'additional_client_info_f': AdditionalClientInfoForm(),
												  'save_btn': 'Add'
												  })
	elif sbm == 'Add' or 'Update':
		сlient = getClient(post)
		if PassportForm(post).is_valid():
			passport = getPassport(post, сlient)
		else:
			print('passport not created')
		if sbm == 'Update':
			print('Update')
			# //get job, get address id, get address
			jobInfo = updateOrCreateJobInfo(post, '', сlient)
			print(jobInfo.address.id)
			updateOrCreateJobAddressObj(post,2, jobInfo.address.id)
		if 	sbm == 'Add':
			print('Add')
			jobAddress = updateOrCreateAddressObj(post=post, counterp=2, clientp=None)
			jobInfo = updateOrCreateJobInfo(post, 0, сlient)
			jobInfo.address = jobAddress
			jobInfo.save()
		# 	create address create job with address
		#
		# jobAddress = updateOrCreateJobAddressObj()
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
	if btn == DELETE_GEN_DOC:
		deleteGenDoc(gen_doc_id)
	return HttpResponseRedirect('/clients/');

#https://github.com/csev/dj4e-samples/blob/master/form/views.py
@login_required
def edit_client_page(request, client_id):
	client_inst = Client.objects.get(id=client_id);
	clientHasPassport = hasattr(client_inst, 'passport')
	clientHasNotJob = hasattr(client_inst, 'jobinfo')
	print('clientHasNotJob: '+ str(clientHasNotJob))
	passportForm = getForm(clientHasPassport, 'PassportForm', client_inst, 'passport')
	regAddressForm = getRegAddressForm(clientHasPassport, client_inst)
	jobInfoForm = getFormByForeignKey(client_inst, 'JobInfo', 'JobInfoForm')
	addressInst = jobInfoForm.instance.address
	addressForm = AddressForm(instance=addressInst, counter=2)
	return render(request, 'addClient.html', {'all_clients': Client.objects.all(),
												  'client_f': ClientForm(instance=client_inst),
												  'passport_f': passportForm,
												  'registration_addr_f': regAddressForm,
												  'job_addr_f': addressForm,
												  'job_f': jobInfoForm,
												  'bankdetail_f': BankDetailForm(),
												  'approver_f': ApproverForm(),
												  'credit_f': IpotekaForm(),
												  'relative_f': ClientRelativeForm(),
												  'rental_f': RentalIncomeForm(),
												  'pension_f': PensionValueForm(),
												  'imm_prop_f': ImmovablePropForm(),
												  'car_f': AutoForm(),
												  # 's_f': StbeTestForm(),
												  # 'credit_f': credits_factory,
												  # 'client_f': client_form_set,
												  # 'address_f': address_factory,
												  # 'postaddress_f': post_address_factory,
												  # 'bankdetail_f': bank_detail_factory,
												  # 'orginfo_f': organization_factory,
												  'additional_client_info_f': AdditionalClientInfoForm(),
											      'save_btn':'Update'
												  })

@login_required
def generateReport(request):
	client_ids, doc_ids = getCheckedItems(request)
	for client_id in client_ids:
		for doc_id in doc_ids:
			writeClientDoc(client_id, doc_id)
	return HttpResponseRedirect('/clients/');

def deleteChecked(request):
	client_ids, doc_ids = getCheckedItems(request)
	clients = Client.objects.filter(id__in=client_ids)
	clients.delete()
	docs = Document.objects.filter(id__in=doc_ids)
	docs.delete()
	return HttpResponseRedirect('/clients/');


def login(request):
	return render(request, 'accounts/login.html')
