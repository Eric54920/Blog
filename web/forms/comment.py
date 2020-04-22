from django import forms
from web import models


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.ArticleComments
        exclude = ['user', 'parent', 'reply', 'article', 'create_time']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == 'web_site':
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['placeholder'] = '网址 http(s)://'
                continue
            if name == "content":
                field.widget.attrs['rows'] = '3'
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '%s' % (field.label,)