import os
from mainapp.mainapp.settings import *
from django.contrib.auth.models import User
# for file in os.listdir(STATIC_DIR):
#     if file:
#         print(os.path.join(STATIC_DIR, file))


user = User.objects.create_user('myusername', 'myemail@crazymail.com', 'mypassword')
user.first_name = 'John'
user.last_name = 'Citizen'
user.save()