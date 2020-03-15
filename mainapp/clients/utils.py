from clients.forms import *
from clients.models import *
import json
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

def updateOrCreateAddressObj(post, counterp, clientp):
	address = Address.objects.update_or_create(
	    client = clientp,
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
	passport.instance.registration_address = updateOrCreateAddressObj(post=post, counterp=0, clientp=сlient)
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
									 client_inst.passport, 'registration_address')
	return regAddressForm;

def getForm(isExist, formClass, instance, attr):
	return globals()[formClass](instance=getattr(instance, attr)) \
		if isExist \
		else globals()[formClass];

def getObjectByClient(client_inst, modelClass):
	related__filter = globals()[modelClass].objects.select_related().filter(client=client_inst)
	return related__filter[0] if len(related__filter)>0 else None;

def getFormByForeignKey(client_inst, modelClass, formClass, counter = ''):
	inst = getObjectByClient(client_inst, modelClass)
	return globals()[formClass](counter=counter) if inst is None else  globals()[formClass](instance=inst);

def getCheckedItems(request):
	client_view_params = request.body.decode('utf-8')
	json_view_params = json.loads(client_view_params)
	client_ids = json_view_params['checkedClients']
	doc_ids = json_view_params['checkedDocs']
	return client_ids, doc_ids