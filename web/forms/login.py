from django import forms
from web.models import User
from django.core.validators import RegexValidator, ValidationError
from web.utils.encrypt import sha256

class LoginForm(forms.ModelForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        curr_user = User.objects.filter(username=username).first()
        if not curr_user:
            raise ValidationError("用户不存在")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return sha256(password)

    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)