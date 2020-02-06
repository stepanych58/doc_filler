from django.conf.urls import url
from login_auth import views as login_views
from django.conf import settings
from django.urls import path

urlpatterns = [
path(r'login/', login_views.login, name='login'),
path(r'logout/', login_views.logout, name='logout'),
]
