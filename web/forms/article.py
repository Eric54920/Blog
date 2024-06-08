from django import forms
from web import models


class ArticleForm(forms.ModelForm):

    class Meta:
        model = models.Article
        exclude = ['author', 'is_show']
        widgets = {
            'tags': forms.HiddenInput(attrs={'type': 'hidden', 'class': 'all-tags'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'create_time':
                field.widget.attrs['id'] = 'pub-time'
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = f'请选择{field.label}'
                continue
            old_class = field.widget.attrs.get('class', "")
            field.widget.attrs['class'] = f'{old_class} form-control'
            field.widget.attrs['placeholder'] = f'请输入{field.label}'
