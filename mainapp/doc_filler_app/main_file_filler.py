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
		clients_file_name = str(p_client.first_name) + ' ' + \
                                    str(p_client.last_name) + '_' + str(
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
        clients_file_name = str(client.first_name) + ' ' + str(client.last_name) + \
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
        read['str16'] = client.passport.serial + ' ' + client.passport.number #'серия номер паспорта'
        read['str17'] = client.passport.date_of #'дата выдачи'
        read['str18'] = 'код подразделения'
        read['str19'] = client.passport._from #'кем выдан'
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

class VTBAnketa:
    
    def write(client, doc):

        path_in_file = os.path.join(PDF_TEMPLATE_DIR, doc.file_name)
        inpt = open(path_in_file, 'rb')
        clients_file_name = str(client.first_name) + ' ' + str(client.last_name) + \
                            '_' + str(doc.file_name)  # date or time
        p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)


        
        reads = PdfFileReader(inpt)
        read = reads.getFormTextFields()
        checkboxes = reads.getFields()

        

##        дефолтные значения ne menyat
        read['Text Field 490'] = ' '        #fio esli menyalos
        read['Text Field 473'] = ' '        #reklama
        read['Text Field 475'] = ' '        #inoe
        read['Text Field 493'] = ' '
        read['Text Field 494'] = ' '
        read['Text Field 492'] = ' '
        read['Text Field 496'] = ' '
        read['Text Field 497'] = ' '
        read['Text Field 498'] = ' '
        read['Text Field 50910'] = ' '
        read['Text Field 50610'] = ' '
        read['Text Field 505'] = ' '
        read['Text Field 504'] = ' '
        read['Text Field 506'] = ' '
        for i in range(11, 21, 1):
            read['Text Field 50' + str(i)] = ' ' 


        
##Заемщик\созаемщик
        checkboxes['Check Box 136'] = '/Yes' #zaemschik
        checkboxes['Check Box 137'] = '/Yes' #sozaemschik
        checkboxes['Check Box 97'] = '/Yes' #не убирать
##########        Адрес
        checkboxes['Check Box 138'] = '/Yes' #fakt adres sovpadaet s registr

############Основания для проживания
        checkboxes['Check Box 101'] = '/Yes' #соц наем
        checkboxes['Check Box 102'] = '/Yes' #коммерческий наем
        checkboxes['Check Box 103'] = '/Yes' #собственность
        checkboxes['Check Box 104'] = '/Yes' #у родственников
        checkboxes['Check Box 105'] = '/Yes' #иное, отразить в Листе дополнений
######        Семейное положение
        checkboxes['Check Box 106'] = '/Yes' #женат\замужем
        checkboxes['Check Box 107'] = '/Yes' #в разводе
        checkboxes['Check Box 108'] = '/Yes' #вдовец\вдова
        checkboxes['Check Box 109'] = '/Yes' #гражданский брак
        checkboxes['Check Box 110'] = '/Yes' #холост\не замужем

##        Брачный договор
        checkboxes['Check Box 111'] = '/Yes' # есть
        checkboxes['Check Box 112'] = '/Yes' #нет
##        Изменялась фамилия
        checkboxes['Check Box 113'] = '/Yes' #да
        checkboxes['Check Box 114'] = '/Yes' #нет
        #Дети совместно проживают
            #первый ребенок
        checkboxes['Check Box 115'] = '/Yes' #да
        checkboxes['Check Box 116'] = '/Yes' #net
##            второй ребенок
        checkboxes['Check Box 117'] = '/Yes' #da
        checkboxes['Check Box 118'] = '/Yes' #net
##            третий ребенок
        checkboxes['Check Box 119'] = '/Yes' #da
        checkboxes['Check Box 120'] = '/Yes' #net
############Образование
        checkboxes['Check Box 121'] = '/Yes' #nizhe srednego
        checkboxes['Check Box 122'] = '/Yes' #srednee
        checkboxes['Check Box 123'] = '/Yes' #srednee spec
        checkboxes['Check Box 124'] = '/Yes' #neokon vishee
        checkboxes['Check Box 125'] = '/Yes' #highest
        checkboxes['Check Box 126'] = '/Yes' #neskolko high
        checkboxes['Check Box 127'] = '/Yes' #dop vish
        checkboxes['Check Box 128'] = '/Yes' #uchenaya stepen
        checkboxes['Check Box 129'] = '/Yes' #MBA
        checkboxes['Check Box 130'] = '/Yes' #inoe
################занятонсть
        checkboxes['Check Box 131'] = '/Yes' #yavlyatsya zarplatnym proektom
        checkboxes['Check Box 132'] = '/Yes' #ne yavlyaetsa
############Место работы
        checkboxes['Check Box 133'] = '/Yes' #ispytatelny srok
        checkboxes['Check Box 134'] = '/Yes' # ne ispytatelny srok
        checkboxes['Check Box 139'] = '/Yes' #по найму бессрочно
        checkboxes['Check Box 140'] = '/Yes' #по найму срочно
        checkboxes['Check Box 141'] = '/Yes' #ИП
        checkboxes['Check Box 142'] = '/Yes' #собственность бизнеса
######        Сфера деятельности организации
        checkboxes['Check Box 144'] = '/Yes' #армия
        checkboxes['Check Box 145'] = '/Yes' #ИТ
        checkboxes['Check Box 146'] = '/Yes' #Консалтинг
        checkboxes['Check Box 147'] = '/Yes' #Медицина
        checkboxes['Check Box 148'] = '/Yes' #наука
        checkboxes['Check Box 149'] = '/Yes' #образование
        checkboxes['Check Box 150'] = '/Yes' #строительство
        checkboxes['Check Box 151'] = '/Yes' #отповая розничная культура
        checkboxes['Check Box 152'] = '/Yes' #органы власти и управления
        checkboxes['Check Box 153'] = '/Yes' #охранная деятельность
        checkboxes['Check Box 154'] = '/Yes' #предприятия ТЭК
        checkboxes['Check Box 155'] = '/Yes' #промышленность и машиностроение
        checkboxes['Check Box 156'] = '/Yes' #социальная сфера
        checkboxes['Check Box 157'] = '/Yes' #транспорт
        checkboxes['Check Box 158'] = '/Yes' #туризм
        checkboxes['Check Box 159'] = '/Yes' #услуги
        checkboxes['Check Box 160'] = '/Yes' #финансы, банки, стразование
        checkboxes['Check Box 161'] = '/Yes' #другие отрасли
######################Численность персонала
        checkboxes['Check Box 162'] = '/Yes' #do 10        
        checkboxes['Check Box 163'] = '/Yes' #11-50
        checkboxes['Check Box 164'] = '/Yes' #51-100
        checkboxes['Check Box 165'] = '/Yes' #101-500
        checkboxes['Check Box 166'] = '/Yes' #501-1000
        checkboxes['Check Box 167'] = '/Yes' #>1000
################Срок существования организации
        checkboxes['Check Box 168'] = '/Yes' # до 2 лет
        checkboxes['Check Box 169'] = '/Yes' #от 2 до 5 лет
        checkboxes['Check Box 170'] = '/Yes' #свыше 5 лет
################Дополнительное место работы
        checkboxes['Check Box 171'] = '/Yes' #имею
        checkboxes['Check Box 172'] = '/Yes' # не имею
##########Денежные средства (с учетом первоначального взноса)
        checkboxes['Check Box 17310'] = '/Yes' #имею
        checkboxes['Check Box 174'] = '/Yes' #не имею#
    ####################Автомобиль
        checkboxes['Check Box 175'] = '/Yes' #есть
        checkboxes['Check Box 176'] = '/Yes' #нет
##########Недвижисое имущество
        checkboxes['Check Box 1731011'] = '/Yes' #есть
        checkboxes['Check Box 173'] = '/Yes' #нет

############Основания возниконовения права на имущество        
        checkboxes['Check Box 177'] = '/Yes' #покупка
        checkboxes['Check Box 178'] = '/Yes' #приватизация
        checkboxes['Check Box 179'] = '/Yes' #наследство
        checkboxes['Check Box 180'] = '/Yes' #дарение
        checkboxes['Check Box 181'] = '/Yes' #иное
##############процедура бонкротства
        checkboxes['Check Box 182'] = '/Yes' #применялось
        checkboxes['Check Box 183'] = '/Yes' #не применялось
################Алиментные обязательства
        checkboxes['Check Box 184'] = '/Yes' #yest
        checkboxes['Check Box 185'] = '/Yes' #net
################Не редаткировать. Принять условия соглашения
        checkboxes['Check Box 186'] = '/Yes' #иное
        checkboxes['Check Box 187'] = '/Yes' #иное
        checkboxes['Check Box 189'] = '/Yes' #согласие на обработку ПДн
######################Представитель
        checkboxes['Check Box 188'] = '/Yes' #есть представитель




        

        

################Клиент        
        read['Text Field 470'] = 'stepen rodstva s zaemschikom'
        read['Text Field 471'] = client.last_name + ' ' + client.first_name + \
                                 ' ' + client.part_name
        read['Text Field 472'] = 'дата рождения'
        read['Text Field 474'] = 'snils'
        read['Text Field 476'] = 'INN'
        read['Text Field 477'] = 'index'
        read['Text Field 478'] = 'strana'
        read['Text Field 479'] = 'oblast'
        read['Text Field 480'] = 'rayon'
        read['Text Field 481'] = 'naselenny punkt'
        read['Text Field 482'] = 'street'
        read['Text Field 483'] = 'number of home'
        read['Text Field 484'] = 'korpus'
        read['Text Field 485'] = 'flat'
        read['Text Field 486'] = 'phone'
        read['Text Field 487'] = 'home phone reg'
        read['Text Field 488'] = 'home phone prozhivanie'
        read['Text Field 489'] = 'work phone'
        read['Text Field 490'] = 'e-mail'
        if checkboxes['Check Box 113'] =='/Yes': #изменялась ли фамилмя
            read['Text Field 491'] = 'FIO'
            read['Text Field 492'] = 'god izmeneniya'
##################Дети
        read['Text Field 493'] = 'data rozhdeniya 1go rebenka'
        read['Text Field 494'] = 'data rozhdeniya 2go rebenka'

################Зарплатный проект
        if checkboxes['Check Box 131'] == '/Yes':
            read['Text Field 496'] = 'nomer karty'
####################Работа
        if checkboxes['Check Box 136'] == '/Yes':
            read['Text Field 497'] = 's'
            read['Text Field 498'] = 'do'
        if checkboxes['Check Box 138'] == '/Yes':
            read['Text Field 499'] = '% buisness'
        read['Text Field 500'] = 'должность'
        read['Text Field 501'] = 'среднемесячный доход'
        read['Text Field 502'] = "стаж работы на текущем месте, лет"
        read['Text Field 50311'] = 'Стаж по профилю, лет'
        read['Text Field 50411'] = 'Общий стаж работы общий, лет'
        read['Text Field 50510'] = 'Название организации'
        read['Text Field 50610'] = 'инн организации'
        read['Text Field 50710'] = 'фактический адрес'
        read['Text Field 50810'] = 'телефон организации'
        read['Text Field 50910'] = 'добавочный номер'
        read['Text Field 5010'] = 'сайт организации'
        if checkboxes['Check Box 151'] == '/Yes':
            read['Text Field 505'] = 'сфера розничной торговли'
        if checkboxes['Check Box 159'] == '/Yes':
            read['Text Field 504'] = 'уточните сферу'
        if checkboxes['Check Box 161'] == '/Yes':
            read['Text Field 503'] = 'Уточните'

            
######################Активы
        if checkboxes['Check Box 173'] == '/Yes':
            read['Text Field 5011'] = 'Наличные средства, сумма, руб'
            read['Text Field 5012'] = 'Банк №1'
            read['Text Field 5013'] = 'Банк №2'
            read['Text Field 5014'] = 'Сумма'
            read['Text Field 5015'] = 'Сумма'
        if checkboxes['Check Box 175'] == '/Yes':
            read['Text Field 5016'] = 'марка'
            read['Text Field 5017'] = 'год приобретения'
            read['Text Field 5018'] = 'стоимость по вашей оценке'
        if checkboxes['Check Box 1731011'] == '/Yes':
            read['Text Field 5019'] = 'Тип объекта недвижимости'
            read['Text Field 5020'] = 'Текущая рыночная стоимость(по вашей оценке)'
        if checkboxes['Check Box 181'] == '/Yes':
            read['Text Field 506'] = 'иное'

######################Представитель
        if checkboxes['Check Box 188'] == '/Yes':
            read['Text Field 5021'] = 'Фио представителя'
########################Согласие на Пдн
        read['Text Field 5026'] = client.last_name + ' ' + client.first_name + \
                                 ' ' + client.part_name #Пдн



        
        
        
        outpt = open(p_file_path, 'wb')
        write = PdfFileWriter()
        set_need_appearances_writer(write)
        for i in range(reads.getNumPages()):
            write.addPage(reads.getPage(i))
            updateCheckboxValues(reads.getPage(i), checkboxes)
            write.updatePageFormFieldValues(reads.getPage(i),read)
        write.write(outpt)
        inpt.close()
        outpt.close()
