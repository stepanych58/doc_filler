from django.forms.widgets import Input, Widget

class ManyValueInput(Widget):
    template_name = 'django/widgets/manyW.html'

class Duration(Widget):
    template_name = 'django/widgets/duration.html'