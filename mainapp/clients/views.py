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
												  'client_f': empty_client_form,
												  'passport_f': empty_passp_form,
												  'registration_addr_f': AddressForm(initial=address_initial, counter=0),
												  'job_addr_f': AddressForm(initial=address_initial, counter=2),
												  'job_post_addr_f': AddressForm(initial=address_initial, counter=3),
												  'job_f': JobInfoForm(counter=0),
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
												  'additional_client_info_f': AdditionalClientInfoForm(),
												  'save_btn': 'Add'
												  })
	elif sbm == 'Add' or 'Update':
		сlient = getClient(post)
		jobInfo = updateOrCreateObjByClient(post, 0, сlient, 'JobInfo')
		credit = updateOrCreateObjByClient(post, '', сlient, 'Ipoteka')
		additionalInfo = updateOrCreateObjByClient(post, '', сlient, 'AdditionalClientInfo')

		if sbm == 'Update':
			print('Update')
			# //get job, get address id, get address
			passport = updateOrCreateObjByClient(post, '', сlient, 'Passport')
			updateOrCreateById(post, 'Address', 0, passport.registration_address.id)
			if jobInfo.address is not None:
				updateOrCreateById(post, 'Address', 2, jobInfo.address.id)
			else:
				print('address dosnt exist for ' + str(сlient.first_name) + ' ' +str(сlient.last_name))
				jobInfo.address = createObj(post, 'Address', AddressForm.Meta.labels.keys(), counter=2)

			if jobInfo.post_address is not None:
				updateOrCreateById(post, 'Address', 3, jobInfo.post_address.id)
			else:
				print('post_address dosnt exist for ' + str(сlient.first_name) + ' ' +str(сlient.last_name))
				jobInfo.post_address = createObj(post, 'Address', AddressForm.Meta.labels.keys(), counter=3)

			if jobInfo.approver is not None:
				updateOrCreateById(post, 'Approver', '', jobInfo.approver.id)
			else:
				print('approver dosnt exist for ' + str(сlient.first_name) + ' ' +str(сlient.last_name))
				jobInfo.approver = createObj(post, 'Approver', ApproverForm.Meta.labels.keys())

			if jobInfo.bank_detail is not None:
				updateOrCreateById(post, 'BankDetail', '', jobInfo.bank_detail.id)
			else:
				print('bank detail doesnt exist for ' + str(сlient.first_name) + ' ' +str(сlient.last_name))
				jobInfo.bank_detail = createObj(post, 'BankDetail', BankDetailForm.Meta.labels.keys())
			jobInfo.save()

		if 	sbm == 'Add':
			print('Add')
			passport = getPassport(post, сlient)
			jobAddress = createObj(post, 'Address', AddressForm.Meta.labels.keys(), counter=2)
			jobPostAddress = createObj(post, 'Address', AddressForm.Meta.labels.keys(), counter=3)
			jobInfo.address = jobAddress
			jobInfo.post_address = jobPostAddress
			jobInfo.approver = createObj(post, 'Approver', ApproverForm.Meta.labels.keys())
			jobInfo.bank_detail = createObj(post, 'BankDetail', BankDetailForm.Meta.labels.keys())
			jobInfo.save()

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
	username = auth.get_user(request).username
	client_inst = Client.objects.get(id=client_id);
	clientHasPassport = hasattr(client_inst, 'passport')
	# clientHasNotJob = hasattr(client_inst, 'jobinfo')
	clientHasAdditionalInfo = hasattr(client_inst, 'additionalclientinfo')
	passportForm = getForm(clientHasPassport, 'PassportForm', client_inst, 'passport')
	regAddressForm = getRegAddressForm(clientHasPassport, client_inst)
	jobInfoForm = getFormByForeignKey(client_inst, 'JobInfo', 0)
	addressInst = jobInfoForm.instance.address
	organizationPostAddr = jobInfoForm.instance.post_address
	organizationPostAddrForm = AddressForm(instance=organizationPostAddr, counter=3)
	addressForm = AddressForm(instance=addressInst, counter=2)
	additionalInfoForm = getFormWithoutCounter(clientHasAdditionalInfo, 'AdditionalClientInfoForm',
								 client_inst, 'additionalclientinfo')
	approverForm = ApproverForm(instance=jobInfoForm.instance.approver)
	bankDetailForm = BankDetailForm(instance=jobInfoForm.instance.bank_detail)

	return render(request, 'addClient.html', {'all_clients': Client.objects.all(),
												  'client_f': ClientForm(instance=client_inst),
												  'passport_f': passportForm,
												  'registration_addr_f': regAddressForm,
												  'job_addr_f': addressForm,
												  'job_post_addr_f': organizationPostAddrForm,
												  'job_f': jobInfoForm,
												  'bankdetail_f': bankDetailForm,
												  'approver_f': approverForm,
												  'credit_f': IpotekaForm(),
												  'relative_f': ClientRelativeForm(),
												  'rental_f': RentalIncomeForm(),
												  'pension_f': PensionValueForm(),
												  'imm_prop_f': ImmovablePropForm(),
												  'car_f': AutoForm(),
												  'additional_client_info_f': additionalInfoForm,
											      'save_btn':'Update',
												  'username': username,
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


# def delete(self, request, *args, **kwargs):
#
# 	self.object = self.get_object()
# 	if self.request.user != self.object.author:
# 		return self.handle_no_permission()
# 	success_url = self.get_success_url()
# 	self.object.delete()
# 	return HttpResponseRedirect(success_url)
