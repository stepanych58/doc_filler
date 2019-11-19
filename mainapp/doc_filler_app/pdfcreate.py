from PyPDF2 import PdfFileWriter, PdfFileReader  #Необходимо докачать pip'oм
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
import os
file_name = "out_ids.txt"
sfile = open(file_name,"a") 

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




def writeAlfa(ankteta, out):
    inpt = open(anketa, 'rb')
    reads = PdfFileReader(inpt)
    read = reads.getFormTextFields()
    iterator = 0
    sfile.write(str(read))
    for i in read:
        read[i] = str(iterator)
        #read[i] = str(i)
        iterator +=1
        sfile.write(str(i) +'-' +str(iterator) + '\n')
        print(str(i) +'-' +str(iterator))
        #read['str' + str(i)] = l1st[i]
    #read['Text Field 5424'] = '4'
    print(iterator)
    outpt = open(out, 'wb')
    write = PdfFileWriter()
    set_need_appearances_writer(write)
    for i in range(reads.getNumPages() - 1):   #пока хз почему
        write.addPage(reads.getPage(i))
        write.updatePageFormFieldValues(reads.getPage(i),read)
    write.write(outpt)
    inpt.close()
    outpt.close()
    sfile.close()


if __name__ == "__main__":
    anketa = 'dom_rf_ipoteca.pdf'
    out = '2.pdf'
    writeAlfa(anketa,out)
#    dict1 = {}
#    print('stbe start')
#    dict1 = {'23':'123'}
#    dict1.update({'234':'123'})
#    print('stbe end')
#    print(dict1)
