from django.shortcuts import render, redirect
from accounts.forms import RegisterForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
import pdb
from accounts.ValidateForm import ValidateForm

def register(request):
    form = RegisterForm()

    context = {
        'form' : form
    }

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            print('Je suis valide')
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_conf = form.cleaned_data['password_conf']

            validate = ValidateForm(request)
            validation_form = validate.register_form(first_name=first_name, last_name=last_name, email=email, username=username, password=password, password_conf=password_conf)

            if validation_form:
                user = User.objects.create(first_name=first_name, last_name=last_name, username=username, email=email, password=password)
                user.save()
                # TODO: envoyer un courriel de confirmation
                auth.login(request, user)
                messages.success(request, 'Vous êtes maintenant enregistrés')
                return redirect('dashboard')
            else:
                validate.get_error_messages()
                return redirect('register')






    return render(request, 'accounts/register.html', context)

def login(request):
    pass

def logout(request):
    pass

def dashboard(request):
    return render(request, 'accounts/dashboard.html')


