from django import forms
from web import models


class AboutForm(forms.ModelForm):
    
    class Meta:
        model = models.User
        # fields = "__all__"
        exclude = ['password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for _, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
