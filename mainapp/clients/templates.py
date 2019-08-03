from django.template import Context, Template
from .models import Client

def get_client_link(id):
    link_tmp = Template('<a href="{{client_link}}"> {{ client_value }} <a>')
    client = Client.objects.get(id = id)
    client_link = '/clientInfo/'+str(id);
    client_value = client.first_name + ' ' + client.part_name + client.last_name
    link_cxt = Context({'client_link': client_link,
                        'client_value': client_value})
    return link_tmp.render(link_cxt)