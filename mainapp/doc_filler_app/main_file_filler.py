from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from mainapp.settings import *
import os

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

def writeToPdf(in_file_name, out_file_name):
    #todo if if document.type = pdf file path = then and so on
#    print('start writeToPdf')
    path_in_file = os.path.join(PDF_TEMPLATE_DIR, in_file_name)
    path_out_file = os.path.join(PDF_GENERATED_RESULT_DIR, out_file_name)
    inpt = open(path_in_file, 'rb')
    print(inpt)
    reads = PdfFileReader(inpt)
    read = reads.getFormTextFields()
    Page = reads.getPage(0)
    for i, value in Page.items():
        read['20'] = '19'
        read['1'] = 'Arkadfi'
        read['2'] = 'Аркадий'
        read['undefined_4'] = 'Олегович'
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
#    print('end writeToPdf')


#example to execute
#if __name__ == "__main__":
#   anketa = 'spravka_po_forme_banka.pdf'
#    out = '2.pdf'
#    writeToPdf(anketa, out)
