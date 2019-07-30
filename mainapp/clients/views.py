from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from doc_filler_app.main_file_filler import *
from mainapp.settings import *
import os
from .utils import *

# Create your views here.

#ALL_CLIENTS = Client.objects.all()
#ALL_DOCS = Document.objects.all()

DELETE = 'Delete'
GENERATE = 'Generete Doc'

view_params = {'all_clients': Client.objects.all(),
			   'all_docs': Document.objects.all(),
			   'test_param':'tp',
			   'all_clients_files':ClientsFile.objects.all(),}

def allClients(request, test_param="tp"):
	view_params['all_clients'] = Client.objects.all()
	view_params['all_docs'] = Document.objects.all()
	view_params['all_clients_files'] = ClientsFile.objects.all()
	return render(request, 'clients.html', view_params);

def addClient(request):
	sbm = request.POST['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),})
	p_first_name = request.POST['first_name']
	p_part_name = request.POST['part_name']
	p_last_name = request.POST['last_name']
	client = Client(first_name = p_first_name, part_name = p_part_name, last_name = p_last_name)
	client.save()
	return HttpResponseRedirect('/clients/');


def deleteClient(request, client_id):
	Client.objects.get(id = client_id).delete();

def clientForm(request, client_id):
	btn = request.POST['sbm']
	doc_id = request.POST['doc_id']
	if btn == DELETE:
		deleteClient(request, client_id)
	if btn == GENERATE:
		writeToPdf(client_id, doc_id)
	return HttpResponseRedirect('/clients/');

def createTestData(request):
    create_test_data()
    return HttpResponseRedirect('/clients/');

def clearData(request):
    Client.objects.all().delete()
    Document.objects.all().delete()
    return HttpResponseRedirect('/clients/');

def uploadTemplate(request):
	#add logic to save template in certain directory https://www.programcreek.com/python/example/59557/django.core.files.storage.FileSystemStorage
	if request.method == 'POST':
		uploaded_file = request.FILES['template']
		file_name = os.path.splitext(uploaded_file.name)[0]
		ext = os.path.splitext(uploaded_file.name)[1]
		if ext == PDF_EXT:
			FileSystemStorage(location = PDF_TEMPL_DIR).save(file_name, uploaded_file)
		elif ext == DOC_EXT:
			FileSystemStorage(location = DOC_TEMPL_DIR).save(file_name, uploaded_file)
		elif ext == TXT_EXT:
			FileSystemStorage(location = TXT_TEMPL_DIR).save(file_name, uploaded_file)
		elif ext == EXEL_EXT:
			FileSystemStorage(location = EXEL_TEMPL_DIR).save(file_name, uploaded_file)
		else: view_params['test_param'] = 'No file extentions!'
	return HttpResponseRedirect('/clients/');


