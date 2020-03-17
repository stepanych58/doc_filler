from django.http import QueryDict

from .forms import *
from .models import *
import json

def initDefaults(post, counter='', keys={}):
	defaults = {}
	for key in keys:
		defaults[key] = getPostValue(post,key, counter)
	return defaults

def getPostValue(post, param, counter=''):
	return post.get(param + str(counter))

def updateOrCreateJobInfo(post, counterp, clientp):
	jobinfo = JobInfo.objects.update_or_create(
		client = clientp,
		defaults = {
			'position':getPostValue(post, 'position', counterp),
		}
	)[0];
	return jobinfo;

def updateOrCreatePassport(post, clientp):
	defaults = initDefaults(post, '',PassportForm.Meta.labels.keys())
	print('passport defaults:' + str(defaults))
	print('passport post:' + str(post))
	print('passport keys:' + str(PassportForm.Meta.labels.keys()))
	passport = Passport.objects.update_or_create(
		client = clientp,
		defaults = defaults
	)[0];
	return passport;

def updateOrCreateAddressObj(post, counterp = ''):
	defaults = initDefaults(post, counterp, AddressForm.Meta.labels.keys())
	print('Address defaults:' + str(defaults))
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
	# query_dict = QueryDict('', mutable=True)
	# query_dict.update(defaults)
	# addr = AddressForm(query_dict)
	# if addr.is_valid():
	# 	addr = addr.save()
	# else:
	# 	print(addr)
	# 	print('addr isValid false ')
	# 	print(addr.errors)
	# address = Address.objects.update_or_create(
	# 	id = addr.id,
	# 	defaults =defaults)[0]
	# print('created addrr ' + str(address.id))
	return address;

def updateOrCreateJobAddressObj(post, counterp, addressId):
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
	passport.instance.registration_address = updateOrCreateAddressObj(post=post, counterp=0)
	passport = passport.save()
	return passport

def getClient(post):
	client_id = getPostValue(post=post, param='client_id')
	if client_id is not None and client_id != '':
		сlient = Client.objects.get(id=client_id)
		сlient = updateClient(post, сlient)
	else:
		сlient = ClientForm(post)
		print(post)
		print(сlient)
		сlient = ClientForm(post).save();
	return сlient

def getRegAddressForm(clientHasPassport, client_inst):
	regAddressForm = AddressForm(counter=0)
	if clientHasPassport:
		passportHasAddress = hasattr(client_inst.passport, 'registration_address')
		regAddressForm = getForm(passportHasAddress, 'AddressForm',
									 client_inst.passport, 'registration_address', counter=2)
	return regAddressForm;

def getForm(isExist, formClass, instance, attr, counter=''):
	return globals()[formClass](instance=getattr(instance, attr), counter=counter) \
		if isExist \
		else globals()[formClass](counter=counter);

def getObjectByClient(client_inst, modelClass):
	related__filter = globals()[modelClass].objects.select_related().filter(client=client_inst)
	return related__filter[0] if len(related__filter)>0 else None;

def getFormByForeignKey(client_inst, modelClass, formClass):
	inst = getObjectByClient(client_inst, modelClass)
	return globals()[formClass]() if inst is None else  globals()[formClass](instance=inst);

def getCheckedItems(request):
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	client_ids = json_view_params['checkedClients']
	doc_ids = json_view_params['checkedDocs']
	return client_ids, doc_ids