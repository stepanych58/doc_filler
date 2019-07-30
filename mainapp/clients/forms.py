from django import forms


class UploadTemplateForm(forms.Form):
    #title = forms.CharField(max_length=50, label = 'Template Name')
    template = forms.FileField(label = 'Choose template')
