from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from mainapp.settings import *
import os
from clients.models import *
#PDF TEMPLATE DIR
PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
#PDF GENERETED RESULT DIR
PDF_GENERATED_RESULT_DIR = STATICFILES_DIRS[3]

def set_need_appearances_writer(writer: PdfFileWriter):
    try:
        catalog = writer._root_object
        if "/AcroForm" not in catalog:
            writer._root_object.update({
                NameObject("/AcroForm"): IndirectObject(len(writer._objects), 0, writer)})
        need_appearances = NameObject("/NeedAppearances")
        writer._root_object["/AcroForm"][need_appearances] = BooleanObject(True)
        return writer

    except Exception as e:
        print('set_need_appearances_writer() catch : ', repr(e))
        return writer

def writeToPdf(client_id, doc_id):
	p_client = Client.objects.get(id=client_id)
	p_doc = Document.objects.get(id=doc_id)
	organization = p_client.organizationinfo
	organization_address = organization.address
	organization_postaddress = organization.post_address
	organization_bank_detail = organization.bank_detail
	clients_file_name = str(p_client.first_name) + str(p_client.last_name) + '_' + str(p_doc.file_name)   #date or time
	p_file_path = ''
	if p_doc.file_type == 'pdf':
	  p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)
	client_file = ClientsFile(client = p_client, file_path = p_file_path)
	client_file.save()
	path_in_file = os.path.join(PDF_TEMPLATE_DIR, p_doc.file_name)
	path_out_file = p_file_path
	inpt = open(path_in_file, 'rb')
	reads = PdfFileReader(inpt)
	read = reads.getFormTextFields()
	Page = reads.getPage(0)
	for i, value in Page.items():
		read['1'] = p_client.last_name
		read['2'] = p_client.first_name
		read['undefined_4'] = p_client.part_name
		read['undefined_5'] = p_client.position
		#Организация
		read['1_2'] = organization.full_name
		read['fill_11'] = organization_address.index
		read['fill_12'] = organization_address.city
		read['undefined_6'] = organization_address.street
		read['fill_14'] = organization_address.buildingNumber
		read['fill_15'] = organization_address.housing
		read['fill_16'] = organization_address.structure
		read['fill_17'] = organization_address.flat
		read['fill_25'] = organization.accountent_number
		read['undefined_8'] = organization.hr_number
		read['undefined_9'] = organization.inn_number
		read['fill_28'] = organization_bank_detail.account_number
		read['fill_29'] = organization_bank_detail.correspondent_account_number
		read['fill_30'] = organization_bank_detail.bic
		read['fill_31'] = organization_bank_detail.bank_name
		# почтовый адрес
		read['fill_18'] = organization_postaddress.index
		read['fill_19'] = organization_postaddress.city
		read['undefined_7'] = organization_postaddress.street
		read['fill_21'] = organization_postaddress.buildingNumber
		read['fill_22'] =  organization_postaddress.housing
		read['fill_23'] = organization_postaddress.structure
		read['fill_24'] = organization_postaddress.flat

	# read['1_2'] = наименование организации 1 стр
		# read['2_2'] = наименование организации 2 стр
		# read['fill_11'] = индекс
		# read['fill_12'] = город населенный пункт
		# read['undefined_6'] = улица
		# read['fill_14'] = Номер дома
		# read['fill_15'] = корпус
		# read['fill_16'] = строение
		# read['fill_17'] = офис/квартира

		# почтовый адрес
		# read['fill_18'] = индекс
		# read['fill_19'] = город населенный пункт
		# read['undefined_7'] = улица
		# read['fill_21'] = Номер дома
		# read['fill_22'] = корпус
		# read['fill_23'] = строение
		# read['fill_24'] = офис/квартира

		# read['fill_25'] = телефоны отдела кадров
		# read['undefined_8'] = телефоны бугалтерии
		# read['undefined_9'] = Инн
		# read['fill_28'] = номер расчетного счета
		# read['fill_29'] = номер корреспондентского счета
		# read['fill_30'] = БИК
		# read['fill_31'] = наименование банка, в котором рассчетный счет
		# read['undefined_10'] = офис/квартира

	outpt = open(path_out_file, 'wb')
	write = PdfFileWriter()
	set_need_appearances_writer(write)
	write.addPage(Page)
	write.updatePageFormFieldValues(Page,read)
	write.write(outpt)
	inpt.close()
	outpt.close()
	#return client_file


