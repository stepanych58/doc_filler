from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from doc_filler_app.main_file_filler import *
from mainapp.settings import *
import os
from .utils import *
from .forms import *

#ALL_CLIENTS = Client.objects.all()
#ALL_DOCS = Document.objects.all()

DELETE = 'Delete'
GENERATE = 'Generete Doc'

view_params = {'all_clients': Client.objects.all(),
			   'page_title': 'Clients page',
			   'all_docs': Document.objects.all(),
			   'test_param':'tp',
			   'p_table' : 'clients',
			   'all_clients_files':ClientsFile.objects.all(),}

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
	sbm = request.POST['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),})
	p_first_name = request.POST['first_name']
	p_part_name = request.POST['part_name']
	p_last_name = request.POST['last_name']
	client = Client(first_name = p_first_name, part_name = p_part_name, last_name = p_last_name)
	client.save()
	return HttpResponseRedirect('/clients/');


def deleteClient(client_id):
	Client.objects.get(id = client_id).delete();

def deleteTemplate(template_id):
	Document.objects.get(id = template_id).delete();

def clientForm(request, client_id):
	btn = request.POST['sbm']
	page = request.POST['page']
	doc_id = request.POST.get('doc_id')
	if btn == DELETE and page == 'clients':
		deleteClient(client_id)
	if btn == DELETE and page == 'templates':
		deleteTemplate(client_id)
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
		tmp_name = request.POST['tmp_name']
		file_name = os.path.splitext(uploaded_file.name)[0]
		ext = os.path.splitext(uploaded_file.name)[1]
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
	return render(request, 'test_page.html', {'client_form': ClientForm()})


