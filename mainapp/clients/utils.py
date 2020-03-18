from django.http import QueryDict

from .forms import *
from .models import *
import json


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


def initDefaults(post, counter='', keys={}):
	print('initDefaults start counter : ' + str(counter))
	print(post)
	defaults = {}; empty_fields = {}
	for key in keys:
		print(key)
		postValue = getPostValue(post, key, counter)
		print(postValue)
		if postValue is None or len(postValue) == 0:
			empty_fields[key] = None
		else:
			defaults[key] = postValue
	# print('initDefaults end defaults : ' + str(defaults))
	# print('initDefaults end empty_fields : ' + str(empty_fields))
	return defaults, empty_fields

def getPostValue(post, param, counter=''):
	return post.get(str(param + str(counter)))

def updateOrCreateObjByClient(post, counterp, clientp, modelClass):
	parsedPost = initDefaults(post, counterp, globals()[str(modelClass + 'Form')].Meta.labels.keys())
	defaults = parsedPost[0]
	# print(post)
	# print(modelClass)
	# print(defaults)
	obj = globals()[modelClass].objects.update_or_create(
		client = clientp,
		defaults = defaults)[0];
	emtyFields = parsedPost[1]
	for key in emtyFields:
		setattr(obj, key, emtyFields[key])
	obj.save()
	return obj;

def createAddressObj(post, counterp = ''):
	# defaults = initDefaults(post, counterp, AddressForm.Meta.labels.keys())
	# print('Address defaults:' + str(defaults))
	address = Address.objects.create(
			index = getPostValue(post, 'index', counterp),
			country =getPostValue(post, 'country', counterp),  # страна
			oblast=getPostValue(post, 'oblast', counterp),  # область/республика/край
			rayon=getPostValue(post, 'rayon', counterp),  # район
			city= getPostValue(post, 'city', counterp),  # город/поселок
			street= getPostValue(post, 'street', counterp),  # улица
			buildingNumber= getPostValue(post, 'buildingNumber', counterp),  # номер дома
			housing= getPostValue(post, 'housing', counterp),  # корпус
			structure= getPostValue(post, 'structure', counterp),  # строение
			flat= str(getPostValue(post, 'flat', counterp)));
	return address;

def updateOrCreateAddressObj(post, counterp, addressId):
	address = Address.objects.update_or_create(
	    id = addressId,
		defaults ={
			'index': getPostValue(post, 'index', counterp),
			'country': getPostValue(post, 'country', counterp),  # страна
			'oblast': getPostValue(post, 'oblast', counterp),  # область/республика/край
			'rayon': getPostValue(post, 'rayon', counterp),  # район
			'city': getPostValue(post, 'city', counterp),  # город/поселок
			'street': getPostValue(post, 'street', counterp),  # улица
			'buildingNumber': getPostValue(post, 'buildingNumber', counterp),  # номер дома
			'housing': getPostValue(post, 'housing', counterp),  # корпус
			'structure': getPostValue(post, 'structure', counterp),  # строение
			'flat': str(getPostValue(post, 'flat', counterp))  # квартира/офис
		}
	)[0]
	return address;

def updateClient(post, client):
	client.first_name = getPostValue(post, 'first_name');
	client.last_name = getPostValue(post, 'last_name');
	client.part_name = getPostValue(post, 'part_name');
	client.save()
	return client;

def getPassport(post, сlient):
	passport = PassportForm(post)
	passport.instance.client = сlient
	passport.instance.registration_address = createAddressObj(post=post, counterp=0)
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

def getRegAddressForm(clientHasPassport, client_inst):
	regAddressForm = AddressForm(counter=0)
	if clientHasPassport:
		passportHasAddress = hasattr(client_inst.passport, 'registration_address')
		regAddressForm = getForm(passportHasAddress, 'AddressForm',
									 client_inst.passport, 'registration_address', counter=0)
	return regAddressForm;

def getForm(isExist, formClass, instance, attr, counter=''):
	return globals()[formClass](instance=getattr(instance, attr), counter=counter) \
		if isExist \
		else globals()[formClass](counter=counter);

def getObjectByClient(client_inst, modelClass):
	related__filter = globals()[modelClass].objects.select_related().filter(client=client_inst)
	return related__filter[0] if len(related__filter)>0 else None;

def getFormByForeignKey(client_inst, modelClass, counter=''):
	inst = getObjectByClient(client_inst, modelClass)
	formClass = modelClass + 'Form'
	return globals()[formClass](counter=counter) if inst is None else  globals()[formClass](instance=inst,
																							counter=counter);

def getCheckedItems(request):
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	client_ids = json_view_params['checkedClients']
	doc_ids = json_view_params['checkedDocs']
	return client_ids, doc_ids