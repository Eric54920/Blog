from django import forms
from web import models


class AlbumForm(forms.ModelForm):
    
    class Meta:
        model = models.Album
        fields = ['title', 'intro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'
