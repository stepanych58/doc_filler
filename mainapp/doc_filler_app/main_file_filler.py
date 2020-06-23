from PyPDF2 import PdfFileWriter, PdfFileReader
from PyPDF2.generic import BooleanObject, NameObject, IndirectObject
from mainapp.settings import *
import os
from clients.models import *
# PDF TEMPLATE DIR
from clients.utils import *

PDF_TEMPLATE_DIR = STATICFILES_DIRS[8]
# PDF GENERETED RESULT DIR
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

	print('dasdas')



class SberPoFormeBanka:
	def write(client, anketa):
		jobInfo = getObjectByClient(client, 'JobInfo');
		# print(jobInfo.__dict__)
		jobaddress = Address.objects.get(id=jobInfo.address_id)
		bankdetail = BankDetail.objects.get(id=jobInfo.bank_detail_id)

		# organization = client.organizationinfo
		# organization_address = organization.address
		# organization_postaddress = organization.post_address
		# organization_bank_detail = organization.bank_detail
		clients_file_name = str(client.first_name) + ' ' + \
							str(client.last_name) + '_' + str(
			anketa.file_name)  # date or time
		p_file_path = ''
		if anketa.file_type == 'pdf':
			p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)
		client_file = ClientsFile(client=client, file_path=p_file_path)
		client_file.save()
		path_in_file = os.path.join(PDF_TEMPLATE_DIR, anketa.file_name)
		path_out_file = p_file_path
		inpt = open(path_in_file, 'rb')
		reads = PdfFileReader(inpt)
		read = reads.getFormTextFields()
		Page = reads.getPage(0)
		for i, value in Page.items():
			print(read)
			read['undefined_2']=''
			read['undefined_3']=''
			read['20']=''
			read['1'] = client.last_name
			read['2'] = client.first_name
			read['undefined_4'] = client.part_name
			read['undefined_5'] = jobInfo.position
			# Организация
			read['1_2'] = jobInfo.full_name
			read['2_2'] = '' #продолжение поля 1_2
			read['fill_11'] = jobaddress.index
			read['fill_12'] = jobaddress.city
			read['undefined_6'] = jobaddress.street
			read['fill_14'] = jobaddress.buildingNumber
			read['fill_15'] = jobaddress.housing
			read['fill_16'] = jobaddress.structure
			read['fill_17'] = jobaddress.flat
			read['fill_25'] = jobInfo.account_phone_number
			read['undefined_8'] = jobInfo.hr_phone_number
			read['undefined_9'] = jobInfo.inn_number
			read['fill_28'] = bankdetail.account_number
			read['fill_29'] = bankdetail.correspondent_account_number
			read['fill_30'] = bankdetail.bic
			read['fill_31'] = bankdetail.bank_name
			read['fill_36'] = 'fill_36' #прописью среднемесячный доход за последние N месяцев
			read['fill_41'] = 'fill_41' #Достоверность сведений в справке подтверждаю: Должность
			# почтовый адрес
			read['fill_18'] = jobaddress.index
			read['fill_19'] = jobaddress.city
			read['undefined_7'] = jobaddress.street
			read['fill_21'] = jobaddress.buildingNumber
			read['fill_22'] = jobaddress.housing
			read['fill_23'] = jobaddress.structure
			read['fill_24'] = jobaddress.flat
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
		checkboxes['untitled9'] = '/Yes'  # Квартира
		checkboxes['untitled10'] = '/Yes'  # Дом с участком
		checkboxes['untitled11'] = '/Yes'  # Апартаменты
		checkboxes['untitled12'] = '/Yes'  # Таунхаус
		checkboxes['untitled13'] = '/Yes'  # страховка
		checkboxes['untitled14'] = '/Yes'  # мужчина
		checkboxes['untitled15'] = '/Yes'  # женщина
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
		read['str13'] = client.snils  # 'снилс'
		read['str14'] = client.inn  # inn
		read['str15'] = 'фио при изменении'
		read['str16'] = client.passport.serial + ' ' + client.passport.number  # 'серия номер паспорта'
		read['str17'] = 'дата выдачи'
		read['str18'] = 'код подразделения'
		read['str19'] = client.passport._from  # 'кем выдан'
		read['str20'] = 'адрес регистрации'
		read['str21'] = 'адрес проживания'  # lj,bnm
		read['str22'] = 'мобильный'
		read['str23'] = 'регистрац'
		read['str24'] = 'тел жит'
		read['str25'] = 'email'
		read['str62'] = 'кол-во детей'
		read['str26'] = 'регистрац'

		outpt = open(p_file_path, 'wb')
		write = PdfFileWriter()
		set_need_appearances_writer(write)
		for i in range(reads.getNumPages() - 1):  # пока хз почему
			write.addPage(reads.getPage(i))
			updateCheckboxValues(reads.getPage(i), checkboxes)
		write.updatePageFormFieldValues(reads.getPage(0), read)
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
		read['Text Field 490'] = ' '  # fio esli menyalos
		read['Text Field 473'] = ' '  # reklama
		read['Text Field 475'] = ' '  # inoe
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
		checkboxes['Check Box 136'] = '/Yes'  # zaemschik
		checkboxes['Check Box 137'] = '/Yes'  # sozaemschik
		checkboxes['Check Box 97'] = '/Yes'  # не убирать
		##########        Адрес
		checkboxes['Check Box 138'] = '/Yes'  # fakt adres sovpadaet s registr

		############Основания для проживания
		checkboxes['Check Box 101'] = '/Yes'  # соц наем
		checkboxes['Check Box 102'] = '/Yes'  # коммерческий наем
		checkboxes['Check Box 103'] = '/Yes'  # собственность
		checkboxes['Check Box 104'] = '/Yes'  # у родственников
		checkboxes['Check Box 105'] = '/Yes'  # иное, отразить в Листе дополнений
		######        Семейное положение
		checkboxes['Check Box 106'] = '/Yes'  # женат\замужем
		checkboxes['Check Box 107'] = '/Yes'  # в разводе
		checkboxes['Check Box 108'] = '/Yes'  # вдовец\вдова
		checkboxes['Check Box 109'] = '/Yes'  # гражданский брак
		checkboxes['Check Box 110'] = '/Yes'  # холост\не замужем

		##        Брачный договор
		checkboxes['Check Box 111'] = '/Yes'  # есть
		checkboxes['Check Box 112'] = '/Yes'  # нет
		##        Изменялась фамилия
		checkboxes['Check Box 113'] = '/Yes'  # да
		checkboxes['Check Box 114'] = '/Yes'  # нет
		# Дети совместно проживают
		# первый ребенок
		checkboxes['Check Box 115'] = '/Yes'  # да
		checkboxes['Check Box 116'] = '/Yes'  # net
		##            второй ребенок
		checkboxes['Check Box 117'] = '/Yes'  # da
		checkboxes['Check Box 118'] = '/Yes'  # net
		##            третий ребенок
		checkboxes['Check Box 119'] = '/Yes'  # da
		checkboxes['Check Box 120'] = '/Yes'  # net
		############Образование
		checkboxes['Check Box 121'] = '/Yes'  # nizhe srednego
		checkboxes['Check Box 122'] = '/Yes'  # srednee
		checkboxes['Check Box 123'] = '/Yes'  # srednee spec
		checkboxes['Check Box 124'] = '/Yes'  # neokon vishee
		checkboxes['Check Box 125'] = '/Yes'  # highest
		checkboxes['Check Box 126'] = '/Yes'  # neskolko high
		checkboxes['Check Box 127'] = '/Yes'  # dop vish
		checkboxes['Check Box 128'] = '/Yes'  # uchenaya stepen
		checkboxes['Check Box 129'] = '/Yes'  # MBA
		checkboxes['Check Box 130'] = '/Yes'  # inoe
		################занятонсть
		checkboxes['Check Box 131'] = '/Yes'  # yavlyatsya zarplatnym proektom
		checkboxes['Check Box 132'] = '/Yes'  # ne yavlyaetsa
		############Место работы
		checkboxes['Check Box 133'] = '/Yes'  # ispytatelny srok
		checkboxes['Check Box 134'] = '/Yes'  # ne ispytatelny srok
		checkboxes['Check Box 139'] = '/Yes'  # по найму бессрочно
		checkboxes['Check Box 140'] = '/Yes'  # по найму срочно
		checkboxes['Check Box 141'] = '/Yes'  # ИП
		checkboxes['Check Box 142'] = '/Yes'  # собственность бизнеса
		######        Сфера деятельности организации
		checkboxes['Check Box 144'] = '/Yes'  # армия
		checkboxes['Check Box 145'] = '/Yes'  # ИТ
		checkboxes['Check Box 146'] = '/Yes'  # Консалтинг
		checkboxes['Check Box 147'] = '/Yes'  # Медицина
		checkboxes['Check Box 148'] = '/Yes'  # наука
		checkboxes['Check Box 149'] = '/Yes'  # образование
		checkboxes['Check Box 150'] = '/Yes'  # строительство
		checkboxes['Check Box 151'] = '/Yes'  # отповая розничная культура
		checkboxes['Check Box 152'] = '/Yes'  # органы власти и управления
		checkboxes['Check Box 153'] = '/Yes'  # охранная деятельность
		checkboxes['Check Box 154'] = '/Yes'  # предприятия ТЭК
		checkboxes['Check Box 155'] = '/Yes'  # промышленность и машиностроение
		checkboxes['Check Box 156'] = '/Yes'  # социальная сфера
		checkboxes['Check Box 157'] = '/Yes'  # транспорт
		checkboxes['Check Box 158'] = '/Yes'  # туризм
		checkboxes['Check Box 159'] = '/Yes'  # услуги
		checkboxes['Check Box 160'] = '/Yes'  # финансы, банки, стразование
		checkboxes['Check Box 161'] = '/Yes'  # другие отрасли
		######################Численность персонала
		checkboxes['Check Box 162'] = '/Yes'  # do 10
		checkboxes['Check Box 163'] = '/Yes'  # 11-50
		checkboxes['Check Box 164'] = '/Yes'  # 51-100
		checkboxes['Check Box 165'] = '/Yes'  # 101-500
		checkboxes['Check Box 166'] = '/Yes'  # 501-1000
		checkboxes['Check Box 167'] = '/Yes'  # >1000
		################Срок существования организации
		checkboxes['Check Box 168'] = '/Yes'  # до 2 лет
		checkboxes['Check Box 169'] = '/Yes'  # от 2 до 5 лет
		checkboxes['Check Box 170'] = '/Yes'  # свыше 5 лет
		################Дополнительное место работы
		checkboxes['Check Box 171'] = '/Yes'  # имею
		checkboxes['Check Box 172'] = '/Yes'  # не имею
		##########Денежные средства (с учетом первоначального взноса)
		checkboxes['Check Box 17310'] = '/Yes'  # имею
		checkboxes['Check Box 174'] = '/Yes'  # не имею#
		####################Автомобиль
		checkboxes['Check Box 175'] = '/Yes'  # есть
		checkboxes['Check Box 176'] = '/Yes'  # нет
		##########Недвижисое имущество
		checkboxes['Check Box 1731011'] = '/Yes'  # есть
		checkboxes['Check Box 173'] = '/Yes'  # нет

		############Основания возниконовения права на имущество
		checkboxes['Check Box 177'] = '/Yes'  # покупка
		checkboxes['Check Box 178'] = '/Yes'  # приватизация
		checkboxes['Check Box 179'] = '/Yes'  # наследство
		checkboxes['Check Box 180'] = '/Yes'  # дарение
		checkboxes['Check Box 181'] = '/Yes'  # иное
		##############процедура бонкротства
		checkboxes['Check Box 182'] = '/Yes'  # применялось
		checkboxes['Check Box 183'] = '/Yes'  # не применялось
		################Алиментные обязательства
		checkboxes['Check Box 184'] = '/Yes'  # yest
		checkboxes['Check Box 185'] = '/Yes'  # net
		################Не редаткировать. Принять условия соглашения
		checkboxes['Check Box 186'] = '/Yes'  # иное
		checkboxes['Check Box 187'] = '/Yes'  # иное
		checkboxes['Check Box 189'] = '/Yes'  # согласие на обработку ПДн
		######################Представитель
		checkboxes['Check Box 188'] = '/Yes'  # есть представитель

		################Клиент
		read['Text Field 470'] = 'stepen rodstva s zaemschikom'
		read['Text Field 471'] = client.last_name + ' ' + client.first_name + \
								 ' ' + client.part_name
		read['Text Field 472'] = client.passport.gender  # male/female
		read['Text Field 474'] = client.snils  # 'snils'
		read['Text Field 476'] = client.inn  # 'INN'
		read['Text Field 477'] = 'index'
		read['Text Field 478'] = 'РФ'
		read['Text Field 479'] = 'oblast'
		read['Text Field 480'] = 'rayon'
		read['Text Field 481'] = client.address.city  # 'naselenny punkt'
		read['Text Field 482'] = client.address.street  # 'street'
		read['Text Field 483'] = client.address.buildingNumber  # 'number of home'
		read['Text Field 484'] = 'korpus'
		read['Text Field 485'] = client.address.flat  # 'flat'
		read['Text Field 486'] = 'phone'
		read['Text Field 487'] = 'home phone reg'
		read['Text Field 488'] = 'home phone prozhivanie'
		read['Text Field 489'] = 'work phone'
		read['Text Field 490'] = 'e-mail'
		if checkboxes['Check Box 113'] == '/Yes':  # изменялась ли фамилмя
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
								  ' ' + client.part_name  # Пдн

		outpt = open(p_file_path, 'wb')
		write = PdfFileWriter()
		set_need_appearances_writer(write)
		for i in range(reads.getNumPages()):
			write.addPage(reads.getPage(i))
			updateCheckboxValues(reads.getPage(i), checkboxes)
			write.updatePageFormFieldValues(reads.getPage(i), read)
		write.write(outpt)
		inpt.close()
		outpt.close()


class DomRF_Ipoteca:
	def write(p_client, p_anketa):
		# organization = p_client.organizationinfo
		# organization_address = organization.address
		# organization_postaddress = organization.post_address
		# organization_bank_detail = organization.bank_detail
		clients_file_name = str(p_client.first_name) + ' ' + \
							str(p_client.last_name) + '_' + str(
			p_anketa.file_name)  # date or time
		p_file_path = ''
		if p_anketa.file_type == 'pdf':
			p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)
		client_file = ClientsFile(client=p_client, file_path=p_file_path)
		client_file.save()
		path_in_file = os.path.join(PDF_TEMPLATE_DIR, p_anketa.file_name)
		path_out_file = p_file_path
		inpt = open(path_in_file, 'rb')
		reads = PdfFileReader(inpt)
		read = reads.getFormTextFields()
		Page = reads.getPage(0)
		for i, value in Page.items():
			# 1Роль Заявителя в предполагаемой сделке

			# 2Параметры запрашиваемого кредита
			# сумма кредита
			# срок кредита
			# read['Text Field 5424']
			read['Text Field 5427'] = p_client.last_name
			read['Text Field 5428'] = p_client.first_name
			read['Text Field 5429'] = p_client.part_name
			# Личные Данные заявителя
			read['Text Field 5569'] = p_client.last_name
			read['Text Field 5570'] = p_client.first_name
			read['Text Field 5571'] = p_client.part_name
			# read['Text Field 5572'] = p_client.part_name#дата рождения
			# Предыдущие Ф.И.О.
			read['Text Field 5572'] = p_client.last_name
			read['Text Field 5573'] = p_client.first_name
			read['Text Field 5574'] = p_client.part_name

			# Паспортные данные
			read['Text Field 5574'] = p_client.passport.serial  # серия
			read['Text Field 5575'] = p_client.passport.number  # номер пасспорта
			read['Text Field 5576'] = p_client.passport.date_of.day  # день выдачи
			read['Text Field 5577'] = p_client.passport.date_of.month  # месяц выдачи
			read['Text Field 5578'] = p_client.passport.year  # год выдачи
			read['Text Field 5579'] = p_client.passport._from  # кем выдан 23 символа
			read['Text Field 5584'] = p_client.passport._from  # кем выдан 23 символа
			read['Text Field 5582'] = p_client.passport._from  # кем выдан 10 символов
			read['Text Field 5580'] = p_client.passport.code_of  # код подразделения 3 символа
			read['Text Field 5581'] = p_client.passport.code_of  # код подразделения 3 символа
			read['Text Field 5583'] = p_client.snils.snils_number  # cнилс

			# адрес регистрации
			# адрес проживания
			# контакты
			# read['Text Field 5498'] = p_client.phone_number #мобильный
			# read['Text Field 5499'] = p_client.additionalclientinfo.home_phone_number #домашний
			# read['Text Field 5500'] = p_client.additionalclientinfo.сont_phone_number #контактный
			# read['Text Field 5501'] = p_client.additionalclientinfo.work_phone_number #рабочий
			# read['Text Field 5503'] = p_client.email #email
			# read['Text Field 5502'] = p_client.additionalclientinfo.relations_phone_number #телефон близкого родственника
			# Фио близкого родственника
			# read['Text Field 5505'] = p_client.clientrelative.first_name #имя
			# read['Text Field 5506'] = p_client.clientrelative.part_name #отчество
			# read['Text Field 5507'] = p_client.clientrelative.last_name #фамилия
			# read['Text Field 5504'] = p_client.clientrelative.relation_degree #степень родства

			# Сведения о занятости и доходах Заявителя
			# read['Text Field 5480'] = p_client.additionalclientinfo.work_expireance_years #(год) стаж за последние 5 лет (2 цифры)
			# read['Text Field 5482'] = p_client.additionalclientinfo.work_expireance_month #(месяцев) стаж за последние 5 лет (2 цифры)
			# read['Text Field 5483'] = p_client.additionalclientinfo.work_type_other #тип занятости иное
			# Основная работа (заполняется при наличии)
			# read['Text Field 5484'] = p_client.additionalclientinfo.work_expireance_lw_years  # (год) стаж за последние 5 лет (2 цифры)
			# read['Text Field 5485'] = p_client.additionalclientinfo.work_expireance_lw_month  # (месяцев) стаж за последние 5 лет (2 цифры)

			# Организация
			# read['Text Field 5495'] = organization.full_name
			# read['Text Field 5486'] = organization_address.index
			# read['Text Field 5487'] = organization_address.oblast
			# read['Text Field 5488'] = organization_address.rayon
			# read['Text Field 5489'] = organization_address.city
			# read['Text Field 5490'] = organization_address.street
			# read['Text Field 5491'] = organization_address.buildingNumber
			# read['Text Field 5492'] = organization_address.housing
			# read['Text Field 5493'] = organization_address.structure
			# read['Text Field 5494'] = organization_address.flat
			# read['Text Field 5497'] = organization.hr_number
			# read['Text Field 5496'] = organization.site #адрес сайта
			# read['Text Field 5524'] = organization.inn_number #вид деятельности иное
			# read['Text Field 5522'] = p_client.position #вид деятельности иное
			# read['Text Field 5523'] = p_client.additionalclientinfo.average_income #среднемесячный доход

			# Работа по совместительству (заполняется при наличии) - пока не заполняем
			# Иные доходы Заявителя - пока не заполняем
			# Дополнительная информация о занятости Заявителя (заполняется в случае применения опции «Легкая ипотека») - пока не заполняем

			# Дополнительная информация о доходах от сдачи недвижимости в аренду (заполняется в случае применения опции
			# «Легкая ипотека» и при наличии доходов от сдачи недвижимости в аренду) - пока не заполняем

			# Сведения о расходах Заявителя
			# read['Text Field 5704'] = p_client.additionalclientinfo.aliment  # алименты
			# Информация о кредите/займе
			# read['Text Field 5611'] = p_client.clientcredit.type  # типкредита
			# read['Text Field 5612'] = p_client.clientcredit.creditor_name  # Наименование кредитора
			# read['Text Field 5613'] = p_client.clientcredit.date_start.day  # срок кредита с день
			# read['Text Field 5614'] = p_client.clientcredit.date_start.month  # месяц
			# read['Text Field 5615'] = p_client.clientcredit.date_start.year  # год
			# read['Text Field 5616'] = p_client.clientcredit.date_end.day  # день
			# read['Text Field 5617'] = p_client.clientcredit.date_end.month  # месяц
			# read['Text Field 5618'] = p_client.clientcredit.date_end.year  # год
			# read['Text Field 5620'] = p_client.clientcredit.currency  # валюта
			# read['Text Field 5619'] = p_client.clientcredit.value  # сумма
			# read['Text Field 5621'] = p_client.clientcredit.month_pay  # платеж в месяц
			# read['Text Field 5622'] = p_client.clientcredit.leftover  # остаток
			# Сведения об имуществе Заявителя
			# read['Text Field 5456'] = p_client.additionalclientinfo.immovable_property  # вид недвижимости
			# read['Text Field 5457'] = '100'  # доля в собственности
			# read['Text Field 5458'] = ''  # регион местонахождения
			# read['Text Field 5459'] = ''  # населенный пункт
			# read['Text Field 5460'] = p_client.additionalclientinfo.market_value_of_real_estate  # стоимость
			# авто заявителя
			# read['Text Field 5461'] = p_client.additionalclientinfo.mark_of_car  # марка
			# read['Text Field 5462'] = p_client.additionalclientinfo.model_of_car  # модель
			# read['Text Field 5464'] = p_client.additionalclientinfo.year_of_manufacture_of_car  # год выпуска
			# read['Text Field 5463'] = p_client.additionalclientinfo.car_valuation  # стоимость
		outpt = open(path_out_file, 'wb')
		write = PdfFileWriter()
		set_need_appearances_writer(write)
		write.addPage(Page)
		write.updatePageFormFieldValues(Page, read)
		write.write(outpt)
		inpt.close()
		outpt.close()


class GazpromAnket:

	def write(client, doc):
		path_in_file = os.path.join(PDF_TEMPLATE_DIR, doc.file_name)
		inpt = open(path_in_file, 'rb')
		clients_file_name = str(client.first_name) + ' ' + str(client.last_name) + \
							'_' + str(doc.file_name)  # date or time
		p_file_path = os.path.join(PDF_GENERATED_RESULT_DIR, clients_file_name)

		reads = PdfFileReader(inpt)
		read = reads.getFormTextFields()
		checkboxes = reads.getFields()
		##        checkboxes['chk0'] = '/Yes'
		read['gText1'] = 'Наименование компании-партнёра'
		read['gText2'] = 'ФИО сотрудника компании-партнёра'
		read['gText3'] = 'email@email.com'
		read['Text1'] = read['Text28'] = 'Фамилия'  # client.last_name
		read['Text2'] = 'Имя'  # client.first_name
		read['Text3'] = 'Отчество'  # client.part_name
		##        read['Text28'] = client.first_name + client.part_name
		read['gNum1'] = 9379373737  # телефон партнера
		read['Num1'] = 99999  # запрашиваемая сумма кредита
		read['Num2'] = 122  # количество месяцев срок кредита
		read['Num3'] = 99999  # Предваритаельная стоимость жилья
		read['Text32'] = 'РФ'
		read['Text7'] = 'РФ'
		read['Text8'] = 'oblast'
		read['Text9'] = 'rayon'
		read['Num33'] = 'номер квартиры'  # client.address.flat
		read['Text33'] = 'ulitsa'  # client.address.street
		read['Num32'] = 123  # client.address.buildingNumber
		read['Text44'] = 44  # client.address korpus ??
		read['Text35'] = 'gorod'  # client.address.city
		read['Num6'] = 433  # client.address.flat
		read['Num4'] = 443531  # client.address.index ??
		read['Num7'] = 9061264537  # stacion telefon
		read['email'] = 'email@email.com'  # client.email
		read['Num14'] = 9061264536  # client.phone_number
		read['Text20'] = 'nameOfOrganiz'  # client.OrganizationInfo.full_name
		read['Text21'] = 'address_of_jobs'  # client.OrganizationInfo.address
		read['Num17'] = 'inn'  # client.OrganizationInfo.inn_number
		read['Num18'] = 45523455549  # client.OrganizationInfo.hr_number
		read['Num19'] = 45523455548  # client.OrganizationInfo.phoneJob ??
		# рабочий телефон
		read['Num20'] = 99  # stazh v godah in organization
		read['Num21'] = 11  # stazh v month in organization
		read['Num22'] = 24  # full stazh in years
		read['Num23'] = 11  # full stazh in months
		read['Num24'] = 555555  # client.AdditionalClientInfo.average_income
		read['Num25'] = 12222  # client.AdditionalClinetInfo.aliment
		read['Num26'] = 222222  # client.AdditionalClinetInfo.monetary_obligations
		read['Num27'] = 3608  # client.passport.serial
		read['Num28'] = 128333  # client.passport.number
		read['Num29'] = 640  # str(clent.passport.code_of)[:3]
		read['Num30'] = 128  # str(client.passport.code_of)[4:]
		read['Text31'] = ''  # пока так дальше видно будет

		outpt = open(out, 'wb')
		write = PdfFileWriter()
		set_need_appearances_writer(write)
		for i in range(reads.getNumPages() - 1):  # пока хз почему
			write.addPage(reads.getPage(i))
			updateCheckboxValues(reads.getPage(i), checkboxes)
			write.updatePageFormFieldValues(reads.getPage(i), read)

		write.write(outpt)
		inpt.close()
		outpt.close()
