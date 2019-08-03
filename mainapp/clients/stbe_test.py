from django.template import Context, Template

client_row = Template('<a href={{ client_link }}> {{ client_value }} </a>')
context = Context({'client_link':'/clients/',
                   'client_value': 'Дмитрий Алексеевич Саленый'})
