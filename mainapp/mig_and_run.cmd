del /f db.sqlite3
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser --username stbe0616 --email ibtsni@gmail.com
python manage.py runserver
