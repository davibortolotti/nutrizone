from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .validators import MyPassValidator

class SubmitFood(forms.Form):
	food = forms.CharField(max_length=15)


class RenameFood(forms.Form):
    rename = forms.CharField(max_length=20)
    renmeasure = forms.CharField(max_length=20)


class SignUpForm(UserCreationForm):

    username = forms.CharField(max_length=30, label="Nome de usuário", 
        help_text="Obrigatório. Pode conter caracteres alfanuméricos, _, @, +, . e -.")
    first_name = forms.CharField(max_length=30, label=("Nome"), required=False, help_text='Opcional.')
    last_name = forms.CharField(max_length=30, label=("Sobrenome"), required=False, help_text='Opcional.')
    email = forms.EmailField(max_length=254, help_text='Obrigatório. Informe um e-mail válido')
    password1 = forms.CharField(validators={MyPassValidator}, min_length=6, label=("Senha"), 
        widget=forms.PasswordInput, help_text='Sua senha deve possuir pelo menos 6 caracteres.')
    password2 = forms.CharField(label=("Confirme a Senha"), widget=forms.PasswordInput, 
        help_text=("Coloque a mesma senha acima, para confirmação."))

    error_messages = {
        'password_mismatch': ("As duas senhas não correspondem."),

    }

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


# class LogInForm(AuthenticationForm):

#     # username = forms.CharField(max_length=30, label="Nome de usuário")
    # password = forms.CharField(max_length=30, label=("Senha"), widget=forms.PasswordInput)