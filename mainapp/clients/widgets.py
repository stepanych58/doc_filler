from django.forms.widgets import Select, Widget

class ManyValueInput(Widget):
    template_name = 'django/widgets/manyW.html'

class Duration(Widget):
    template_name = 'django/widgets/duration.html'

class MultipleSelect(Select):
    template_name = 'django/widgets/multipleSelect.html'
    option_template_name = 'django/widgets/data_option.html'
