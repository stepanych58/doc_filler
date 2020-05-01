from django.http import QueryDict

from .forms import *
from .models import *
import json

from django.contrib import auth
client_initial = {'last_name': 'Иванов',
				  'first_name': 'Иван',
				  'part_name': 'Иванович', }
passport_initial = {'serial': '0000',
				  'number': '000000',
				  'v_from': 'ОТДЕЛОМ УФМС ПО САМАРСКОЙ ОБЛАСТИ В ГОРОДЕ НОВОКУЙБЫШЕВСК',
				  'birthday': '1999-01-01',
				  'date_of': '1999-01-01',
				  'code_of': '644-066',
				  }

address_initial = {
			'index': '446100',
			'country': 'Россия',
			'city': 'Самара',
			'street': 'Николая-Панова',
			'buildingNumber': '64',
			'housing': '2',
			'structure': '1',
			'flat': '125',
			'oblast': 'Самарская',
			'rayon': 'Промышленный',}

empty_client_form = ClientForm(initial=client_initial)
empty_passp_form = PassportForm(initial=passport_initial)


class ManyValueTamplate():
	def __init__(self, value, currency):
		self.value= value
		self.currency = currency
	def getValue(self):
		return self.value
	def getCurrency(self):
		return self.currency

	def __str__(self):
		return "[" + str(self.value) + "|" + str(self.currency) + "]";


def getDefaultContext(request):
	context ={
		'all_clients': Client.objects.all(),
		'username': auth.get_user(request).username,
	}
	return context;

def addContextValue(context, key, value):
	context[key] = value;
	return context;

def initDefaults(post, counter='', keys={}):
	# print('initDefaults start counter : ' + str(counter))
	# print(post)
	defaults = {}; empty_fields = {}; mvi_fields ={};
	for key in keys:
		mviValue = False
		print(key)
		postValue = getPostValue(post, key, counter)
		print(postValue)
		if not postValue:
			postValue = getPostValue(post, key, '_mvi')
			mviValue = True
		if not postValue:
			empty_fields[key] = None
		elif mviValue:
			postCurrency = getPostValue(post, key, '_mvi_currency')
			print(" postValue ", postValue)
			print(" postCurrency ", postCurrency)
			mvi_fields[key] = ManyValueTamplate(value=postValue, currency=postCurrency)
		else:
			defaults[key] = postValue
	print('initDefaults end defaults : ' , defaults)
	print('initDefaults end empty_fields : ' , empty_fields)
	resStr=''
	for key in  mvi_fields:
		resStr += str(key) + ": " + str(mvi_fields[key]) + ", "
	print('initDefaults end mvi_fields : ', resStr)
	return defaults, empty_fields, mvi_fields

def getPostValue(post, param, counter=''):
	return post.get(str(param + str(counter)))

def updateOrCreateObjByClient(post, counterp, clientp, modelClass):
	print("updateOrCreateObjByClient start for", modelClass)
	parsedPost = initDefaults(post, counterp, globals()[str(modelClass + 'Form')].Meta.labels.keys())
	defaults = parsedPost[0]
	print(post)
	obj = globals()[modelClass].objects.update_or_create(
		client = clientp,
		defaults = defaults)[0];
	emtyFields = parsedPost[1]
	mviFields = parsedPost[2]
	for key in emtyFields:
		setattr(obj, key, emtyFields[key])
	for key in mviFields:
		manyValueTemplate = mviFields[key]
		setattr(obj, key, ManyValue.objects.create(amount=manyValueTemplate.getValue(), currency=manyValueTemplate.getCurrency()))
	obj.save()
	print(obj)
	return obj;

def createObj(post, modelClass, counter =''):
	fields = globals()[modelClass + 'Form'].Meta.labels.keys()
	obj = globals()[modelClass].objects.create()
	for field in fields:
		setattr(obj, field, getPostValue(post, field, counter))
	obj.save()
	return obj;

# def createAddressObj(post, counterp = ''):
# 	address = Address.objects.create(
# 			index = getPostValue(post, 'index', counterp),
# 			country =getPostValue(post, 'country', counterp),  # страна
# 			oblast=getPostValue(post, 'oblast', counterp),  # область/республика/край
# 			rayon=getPostValue(post, 'rayon', counterp),  # район
# 			city= getPostValue(post, 'city', counterp),  # город/поселок
# 			street= getPostValue(post, 'street', counterp),  # улица
# 			buildingNumber= getPostValue(post, 'buildingNumber', counterp),  # номер дома
# 			housing= getPostValue(post, 'housing', counterp),  # корпус
# 			structure= getPostValue(post, 'structure', counterp),  # строение
# 			flat= str(getPostValue(post, 'flat', counterp)));
# 	return address;

def updateOrCreateById(post, modelName, counterp, id):
	print("updateOrCreateById start ", modelName)
	print("post ", post)
	keys = globals()[modelName + 'Form'].Meta.labels.keys()
	init_defaults = initDefaults(post, counterp, keys)
	defaults = init_defaults[0]
	model = globals()[modelName]
	result = model.objects.update_or_create(
	    id = id,
		defaults = defaults
	)[0]
	return result;

def updateClient(post, client):
	client.first_name = getPostValue(post, 'first_name');
	client.last_name = getPostValue(post, 'last_name');
	client.part_name = getPostValue(post, 'part_name');
	client.save()
	return client;

def getPassport(post, сlient):
	passport = PassportForm(post)
	passport.instance.client = сlient
	passport.instance.registration_address = createObj(post, 'Address', counter=0)
	passport = passport.save()
	return passport

def getClient(post):
	client_id = getPostValue(post=post, param='client_id')
	if client_id is not None and client_id != '':
		сlient = Client.objects.get(id=client_id)
		сlient = updateClient(post, сlient)
	else:
		сlient = ClientForm(post).save();
	return сlient

def getRegAddressForm(client_inst):
	regAddressForm = AddressForm(counter=0)
	if hasattr(client_inst, 'passport'):
		regAddressForm = getForm('AddressForm',
									 client_inst.passport, 'registration_address', counter=0)
	return regAddressForm;

def getForm(formClass, instance, attr, counter=''):
	isExist = hasattr(instance, attr)
	print('isExist: ', isExist)
	return globals()[formClass](instance=getattr(instance, attr), counter=counter) \
		if isExist \
		else globals()[formClass](counter=counter);

def getFormWithoutCounter(formClass, instance, attr):
	isExist = hasattr(instance, attr)
	return globals()[formClass](instance=getattr(instance, attr)) \
		if isExist \
		else globals()[formClass]();

def getObjectByClient(client_inst, modelClass):
	related__filter = globals()[modelClass].objects.select_related().filter(client=client_inst)
	return related__filter[0] if len(related__filter)>0 else None;

def getObjectsByClient(client_inst, modelClass):
	related__filter = globals()[modelClass].objects.select_related().filter(client=client_inst)
	return related__filter;

def getFormByForeignKey(client_inst, modelClass, counter=''):
	inst = getObjectByClient(client_inst, modelClass)
	formClass = modelClass + 'Form'
	return globals()[formClass](counter=counter) if inst is None else  globals()[formClass](instance=inst,
																							counter=counter);
def getFormsByForeignKey(client_inst, modelClass, counter=''):
	insts = getObjectsByClient(client_inst, modelClass)
	formClass = modelClass + 'Form'
	forms = list()
	for inst in insts:
		form = globals()[formClass](counter=counter) if inst is None else  globals()[formClass](instance=inst,
																							counter=counter)
		forms.append(form)
	return forms;

def getCheckedItems(request):
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	client_ids = json_view_params['checkedClients']
	doc_ids = json_view_params['checkedDocs']
	return client_ids, doc_ids