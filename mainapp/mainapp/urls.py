"""mainapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from clients.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', welcomePage),
    path('admin/', admin.site.urls),
    path('clients/', allClients),
    path('addClient/', addClient),
    path('addTemplate/', addTemplate),
    path('deleteClient/<int:client_id>', deleteClient),
    path('clientForm/<int:client_id>', clientForm),
    path('createTestData/', createTestData),
	path('clearData/', clearData),
    path('uploadTemplate/', uploadTemplate),
    path('templates/', allTemplates),
    path('test_page/', testPage),
    path('clientInfo/<int:client_id>', clientInfo),
    path('generateReport/', generateReport),
]

#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)