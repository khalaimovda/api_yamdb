from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.models import User

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[
                self._meta.model.USERNAME_FIELD
            ].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        user = super().save(commit=False)
        password = user.get_new_password()
        user.set_password(password)
        if commit:
            user.save()
        return user
