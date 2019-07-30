from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from doc_filler_app.main_file_filler import *
from mainapp.settings import *

from .create_test_data import *

# Create your views here.

#ALL_CLIENTS = Client.objects.all()
#ALL_DOCS = Document.objects.all()

DELETE = 'Delete'
GENERATE = 'Generete Doc'


def allClients(request, test_param="tp"):
	return render(request, 'clients.html',
				  {'all_clients': Client.objects.all(),
				   'all_docs': Document.objects.all(),
				   'test_param':test_param,
				   'all_clients_files':ClientsFile.objects.all(),});

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
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return HttpResponseRedirect('/clients/');


