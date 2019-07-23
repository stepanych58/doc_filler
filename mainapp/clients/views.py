from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from doc_filler_app.main_file_filler import *
from .utils import *
from mainapp.settings import *
from .create_test_data import *
# Create your views here.

ALL_CLIENTS = Client.objects.all()
ALL_DOCS = Document.objects.all()

DELETE = 'Delete'
GENERATE = 'Generete Doc'


def allClients(request, test_param="tp"):
	return render(request, 'clients.html', {'all_clients': ALL_CLIENTS, 'all_docs': ALL_DOCS,
		'test_param':test_param});

def addClient(request):
	sbm = request.POST['sbm']
	if sbm == 'Add Client':
		return render(request, 'addClient.html', {'all_clients': Client.objects.all(),})
	p_first_name = request.POST['first_name']
	p_part_name = request.POST['part_name']
	p_last_name = request.POST['last_name']
	client = Client(first_name = p_first_name, part_name = p_part_name, last_name = p_last_name)
	client.save()
	return render(request, 'clients.html', {'all_clients': Client.objects.all(), 'all_docs': Document.objects.all(),
		'test_param':'addClient'});


def deleteClient(request, client_id):
	Client.objects.get(id = client_id).delete();

def generateDoc(request, client_id, doc_id):
	anketa = Document.objects.get(id = doc_id).name
	writeToPdf('spravka_po_forme_banka.pdf', 'spravka_po_forme_banka_res.pdf')
	#	writeToPdf(anketa, client_id)

def clientForm(request, client_id):
	btn = request.POST['sbm']
	doc_id = request.POST['doc_id']
	if btn == DELETE:
		deleteClient(request, client_id)
		res = 'delete button is clicked' + 'client_id: ' + str(client_id) + ', doc_id: ' + str(doc_id)
	if btn == GENERATE:
		generateDoc(request, client_id, doc_id)
		res = 'generate button is clicked' + 'client_id: ' + str(client_id) + ', doc_id: ' + str(doc_id) + ' test_util:' + testUtil('test doc filler param') 	
	return render(request, 'clients.html', {'all_clients': Client.objects.all(), 'all_docs': Document.objects.all(),
		 'test_param':res});

def createTestData(request):
    create_test_data()
    return render(request, 'clients.html', {'all_clients': Client.objects.all(), 'all_docs': Document.objects.all(),
		 'test_param':'create test data was clicked'});

def clearData(request):
    #clear data
    Client.objects.all().delete()
    Document.objects.all().delete()
    return render(request, 'clients.html', {'all_clients': Client.objects.all(), 'all_docs': Document.objects.all(),
		 'test_param':'create test data was clicked'});
    
    

