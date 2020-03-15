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
from django.contrib.auth.decorators import login_required, permission_required
from django.conf.urls import include
import login_auth

urlpatterns = [
    path(r'accounts/login/', login),
    path(r'auth/', include('login_auth.urls')),
    path('', welcomePage),
    path('admin/', admin.site.urls),
    path('clients/', allClients),
    path('clientForm/', clientForm),
    path('edit_client_page/<int:client_id>', edit_client_page),
    path('addClient/', addClient),
    path('deleteChecked/', deleteChecked),
    path('generateReport/', generateReport),
    
]


# urlpatterns = [
#     path('', login_required(welcomePage)),
#     path('admin/', admin.site.urls),
#     path('clients/', login_required(allClients)),
#     path('addClient/', login_required(addClient)),
#     path('addTemplate/', login_required(addTemplate)),
#     path('deleteClient/<int:client_id>', login_required(deleteClient)),
#     path('clientForm/<int:client_id>', login_required(clientForm)),
#     path('createTestData/', login_required(createTestData)),
# 	path('clearData/', login_required(clearData)),
#     path('uploadTemplate/', login_required(uploadTemplate)),
#     path('templates/', login_required(allTemplates)),
#     path('test_page/', testPage),
#     path('clientInfo/<int:client_id>', login_required(clientInfo)),
#     path('generateReport/', generateReport),
# ]
#if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
