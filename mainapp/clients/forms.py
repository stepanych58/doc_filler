from django import forms


class UploadTemplateForm(forms.Form):
    #title = forms.CharField(max_length=50, label = 'Template Name')
    template = forms.FileField(label = 'Choose template');

class StbeField(forms.Widget):
    label_value ='stbe1234545566'
    template_name = 'label.html'
    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['label_value'] = self.label_value
        return context


class ClientForm(forms.Form):
     name = forms.CharField(widget=StbeField(), label="stbe")


