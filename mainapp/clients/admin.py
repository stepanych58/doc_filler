from django.contrib import admin

from .models import *

admin.site.register(Client)
admin.site.register(Document)
admin.site.register(ClientsFile)
admin.site.register(Passport)
admin.site.register(SNILS)
admin.site.register(Address)
admin.site.register(PostAddress)
admin.site.register(BankDetail)
admin.site.register(OrganizationInfo)
admin.site.register(AdditionalClientInfo)
