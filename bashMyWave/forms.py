from django import forms


class UploadFileForm(forms.Form):
    file_name = forms.CharField(max_length=50)
    file = forms.FileField()
