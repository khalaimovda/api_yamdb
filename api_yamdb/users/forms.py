from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', )
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[
                self._meta.model.USERNAME_FIELD
            ].widget.attrs['autofocus'] = True

        self.fields['username'].required = True
        self.fields['email'].required = True

    def clean_username(self):
        username = self.cleaned_data.get('username', False)
        if username == 'me':
            raise forms.ValidationError('"me" is forbidden username')
        return username
