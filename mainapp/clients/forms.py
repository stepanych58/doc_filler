from django import forms
from django.forms import CheckboxInput
from .models import *


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
     class Meta:
         model = Client
         fields = ('first_name', 'part_name', 'last_name',)

class ClientChecked(forms.Form):
    cl_check = forms.CharField(widget=CheckboxInput(), label = 'ch_l',required=False)

class UserlistForm(forms.Form):
    users = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,label="Notify and subscribe users to this post:")


