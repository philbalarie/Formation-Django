from django import forms

class RegisterForm(forms.Form):
    first_name = forms.CharField(label='Prénom', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénom'}))
    last_name = forms.CharField(label='Nom de famille', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de famille'}))
    username = forms.CharField(label='Identifiant', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Identifiant'}))
    email = forms.EmailField(label='Courriel', max_length=100, widget=forms.EmailInput(attrs={'class': 'form-control mb-4', 'placeholder':'Courriel'}))
    password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Mot de passe'}))
    password_conf = forms.CharField(label='Confirmation du mot de passe', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder':'Confirmation du mot de passe'}))

class LoginForm(forms.Form):
    username = forms.CharField(label='Identifiant', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control mb-4', 'placeholder': 'Identifiant'}))
    password = forms.CharField(label='Mot de passe', max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control mb-4', 'placeholder' : 'Mot de passe'}))