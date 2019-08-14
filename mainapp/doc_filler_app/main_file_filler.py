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

def updateCheckboxValues(page, fields):

    for j in range(0, len(page['/Annots'])):
        writer_annot = page['/Annots'][j].getObject()
        for field in fields:
            if writer_annot.get('/T') == field:
                writer_annot.update({
                    NameObject("/V"): NameObject(fields[field]),
                    NameObject("/AS"): NameObject(fields[field])
                })

def writeClientDoc(client_id, doc_id):
	p_client = Client.objects.get(id=client_id)
	p_doc = Document.objects.get(id=doc_id)
	writer_class = globals()[p_doc.class_name]
	writer_class.write(p_client, p_doc)

class SberPoFormeBanka:
	def write(client, doc):
		p_client = client
		p_doc = doc
		organization = p_client.organizationinfo
		organization_address = organization.address
		organization_postaddress = organization.post_address
		organization_bank_detail = organization.bank_detail
		clients_file_name = str(p_client.first_name) + str(p_client.last_name) + '_' + str(
			p_doc.file_name)  # date or time
		p_file_path = ''
		if p_doc.file_type == 'pdf':
			p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)
		client_file = ClientsFile(client=p_client, file_path=p_file_path)
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
                    # Организация
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
                    read['fill_22'] = organization_postaddress.housing
                    read['fill_23'] = organization_postaddress.structure
                    read['fill_24'] = organization_postaddress.flat
		outpt = open(path_out_file, 'wb')
		write = PdfFileWriter()
		set_need_appearances_writer(write)
		write.addPage(Page)
		write.updatePageFormFieldValues(Page, read)
		write.write(outpt)
		inpt.close()
		outpt.close()


class AlfaAnketa:
    
    def write(client, doc):
        
        path_in_file = os.path.join(PDF_TEMPLATE_DIR, doc.file_name)
        inpt = open(path_in_file, 'rb')
        clients_file_name = str(client.first_name) + str(client.last_name) + \
                            '_' + str(doc.file_name)  # date or time
        p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)
        
        
        reads = PdfFileReader(inpt)
        read = reads.getFormTextFields()
        checkboxes = reads.getFields()
        checkboxes['chk0'] = '/Yes'
        
    ##    checkboxes['chk1'] = '/Yes' #Созаемщик
    ##    checkboxes['chk2'] = '/Yes' #Поручитель
        checkboxes['untitled9'] = '/Yes' #Квартира  
        checkboxes['untitled10'] = '/Yes' #Дом с участком
        checkboxes['untitled11'] = '/Yes' #Апартаменты
        checkboxes['untitled12'] = '/Yes' #Таунхаус
        checkboxes['untitled13'] = '/Yes' #страховка
        checkboxes['untitled14'] = '/Yes' #мужчина
        checkboxes['untitled15'] = '/Yes' #женщина
    ##    if str(checkboxes['chk1']) == '/Yes' or str(checkboxes['chk2']) == '/Yes':
    ##        read['str0'] = 'фамилия заемщика'
    ##    if checkboxes['chk']
        read['str1'] = 'Сумма кредита'
        read['str2'] = 'срок кредита'
        read['str3'] = 'сумма первоначального взноса'
        read['str4'] = 'стоимость объекта'
        read['str5'] = 'запрашиваемая сумма top up'
        read['str6'] = 'регион приобретения недвижимости'
        read['str7'] = client.last_name
        read['str8'] = client.first_name
        read['str9'] = client.part_name
        read['str10'] = 'дата рождения'
        read['str11'] = 'гражданство'
        read['str12'] = 'место рождения'
        read['str13'] = 'снилс'
        read['str14'] = 'инн'
        read['str15'] = 'фио при изменении'
        read['str16'] = 'серия номер паспорта'
        read['str17'] = 'дата выдачи'
        read['str18'] = 'код подразделения'
        read['str19'] = 'кем выдан'
        read['str20'] = 'адрес регистрации'
        read['str21'] = 'адрес проживания'  #lj,bnm
        read['str22'] = 'мобильный'
        read['str23'] = 'регистрац'
        read['str24'] = 'тел жит'
        read['str25'] = 'email'
        read['str62'] = 'кол-во детей'
        read['str26'] = 'регистрац'

        
        outpt = open(p_file_path, 'wb')
        write = PdfFileWriter()
        set_need_appearances_writer(write)
        for i in range(reads.getNumPages() - 1):   #пока хз почему
            write.addPage(reads.getPage(i))
            updateCheckboxValues(reads.getPage(i), checkboxes)
        write.updatePageFormFieldValues(reads.getPage(0),read)
        write.write(outpt)
        inpt.close()
        outpt.close()
