from django.forms.widgets import Select, Widget

from .choises import CURRANCY_CHOISES

class ManyValueInput(Widget):
    template_name = 'django/widgets/manyW.html'

    def __init__(self, selectedValue='1'):
        Widget.__init__(self)
        self.selectedValue = selectedValue

    def get_context(self, name, value, attrs):
        context = {}
        context['widget'] = {
            'name': name,
            'is_hidden': self.is_hidden,
            'required': self.is_required,
            'value': self.format_value(value),
            'attrs': self.build_attrs(self.attrs, attrs),
            'template_name': self.template_name,
            'currancy_options': CURRANCY_CHOISES,
            'selectedValue': self.selectedValue
        }
        return context

class Duration(Widget):
    template_name = 'django/widgets/duration.html'

class MultipleSelect(Select):
    template_name = 'django/widgets/multipleSelect.html'
    option_template_name = 'django/widgets/data_option.html'
