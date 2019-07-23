import PyPDF2   #Необходимо докачать pip'oм


class write:

    def writeToPdf(self, ankteta, out):
        print('writeToPdf start')
        inpt = open(anketa, 'rb')
        reads = PyPDF2.PdfFileReader(inpt)
        read = reads.getFormTextFields()
        Page = reads.getPage(0)
        print(read.keys())
        for i, value in Page.items():
            read['20'] = '19'
            read['1'] = 'asasdasdasd'
            read['2'] = 'АAsdasdsasd'
            read['undefined_4'] = 'wwwlwlwl'
            read['undefined_5'] = 'ждвлыажыдвлоа'
            read['undefined_11'] = '9999999999999999999'
        outpt = open(out, 'wb')
        write = PyPDF2.PdfFileWriter()
        write.addPage(Page)
        write.updatePageFormFieldValues(Page,read)
        write.write(outpt)        
        inpt.close()
        outpt.close()
        print('writeToPdf end')


if __name__ == "__main__":
    anketa = 'spravka_po_forme_banka.pdf'
    out = '2.pdf'
##    ss = write()
    write().writeToPdf(anketa,out)
##    writeToPdf(anketa, out)
