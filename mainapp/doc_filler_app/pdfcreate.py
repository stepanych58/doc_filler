from PyPDF2 import PdfFileWriter, PdfFileReader  #Необходимо докачать pip'oм
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
import os
file_name = "out_ids.txt"
sfile = open(file_name,"a") 
l1st = ["Саленый Дмитрий Алексеевич, близкий",'999999999', "3", "0", "2500000",
        "ну тут хз", "Бали", "Берендяев", "Степан", "Владимирович",
        "23011996", "РФ", "Лос-Анджелес", "11223442222", "212121211212"
        " 1284578944","", "3636 221122", "11052010",
        "630", "ОУФМС", "LA", "", "9997772211", "", "", "thebest@ofthe.best", "0",
        "", "11223344", "ООО ППП", "услуги", "8463478721", "самый главный", "очень много",
        "ещё больше", "ауди", "2019", "8499000", "", "", "", "", "560000000000",
        "лос-анджелес", "", "", "", "", "", "", "", "", "", "", "", "", "",
        "2313131", "ПАО ВВВ", "ВСЁ", "3213442317", "Генеральный директор", "0"

        ]


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




def writeAlfa(l1st, ankteta, out):
    inpt = open(anketa, 'rb')
    reads = PdfFileReader(inpt)
    read = reads.getFormTextFields()
    iterator = 0
    sfile.write(str(read))
    for i in read:
        #read[i] = str(iterator)
        read[i] = str(i)
        iterator +=1
        #print(read[str(i)])
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



if __name__ == "__main__":
    anketa = 'dom_rf_ipoteca.pdf'
    out = '2.pdf'

    writeAlfa(l1st, anketa,out)
