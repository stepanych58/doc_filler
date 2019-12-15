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

from cms.sitemaps import CMSSitemap
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import path
from clients.views import *
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve


admin.autodiscover()

urlpatterns = [

    url(r'^sitemap\.xml$', sitemap,
        {'sitemaps': {'cmspages': CMSSitemap}}),

    path('1',testPage ),
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
urlpatterns += i18n_patterns(
    url(r'^admin/', admin.site.urls),  # NOQA
    url(r'^', include('cms.urls')),
)

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

if settings.DEBUG:
    urlpatterns = [
        url(r'^media/(?P<path>.*)$', serve,
            {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
        ] + staticfiles_urlpatterns() + urlpatterns
