from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
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
	return render(request, 'clients.html', {'all_clients': ALL_CLIENTS, 'all_docs': ALL_DOCS,
		'test_param':'addClient'});


def deleteClient(request, client_id):
	Client.objects.get(id = client_id).delete();
	return render(request, 'clients.html', {'all_clients': ALL_CLIENTS,});

def generateDoc(request, client_id, doc_id):
	res = 'generate button is clicked' + "  s"
	allClients(request, res);

def clientForm(request, client_id):
	btn = request.POST['sbm']
	doc_id = request.POST['doc_id']
	if btn == DELETE:
		deleteClient(request, client_id)
		res = 'delete button is clicked' + 'client_id: ' + str(client_id) + ', doc_id: ' + str(doc_id)
	if btn == GENERATE:
		generateDoc(request, client_id, doc_id)
		res = 'generate button is clicked' + 'client_id: ' + str(client_id) + ', doc_id: ' + str(doc_id)	
	return render(request, 'clients.html', {'all_clients': ALL_CLIENTS, 'all_docs': ALL_DOCS,
		 'test_param':res});

