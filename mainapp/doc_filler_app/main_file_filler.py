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
		read['20'] = '19'
		read['1'] = p_client.last_name
		read['2'] = p_client.first_name
		read['undefined_4'] = p_client.part_name
		read['undefined_5'] = 'Ничего не делаю'
		read['undefined_11'] = '9999999999999999999'
	outpt = open(path_out_file, 'wb')
	write = PdfFileWriter()
	set_need_appearances_writer(write)
	write.addPage(Page)
	write.updatePageFormFieldValues(Page,read)
	write.write(outpt)
	inpt.close()
	outpt.close()
	#return client_file


