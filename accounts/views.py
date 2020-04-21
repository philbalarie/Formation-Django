from django.shortcuts import render, redirect
from accounts.forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib import messages, auth
import pdb
from accounts.ValidateForm import ValidateForm
from travels.models import Order, OrderTravel, Travel
from django.contrib.auth.decorators import login_required

def register(request):

    if request.user.is_authenticated:
        return redirect('dashboard')

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
                messages.success(request, 'Vous êtes maintenant enregistré.')
                return redirect('dashboard')
            else:
                validate.get_error_messages()
                return redirect('register')

    return render(request, 'accounts/register.html', context)

def login(request):

    form = LoginForm()

    context = {
        'form' : form
    }

    if request.method == 'POST':

        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                messages.success(request,'Vous êtes maintenant connecté.')
                return redirect('dashboard')
            else:
                messages.error(request, 'Identifiants erronés')
                return redirect('login')

    return render(request, 'accounts/login.html', context)

@login_required
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'Vous êtes maintenant déconnecté.')
        return redirect('index')

@login_required
def dashboard(request):

    if request.method == 'GET':
        if request.GET.get('p') == 'success':
            messages.success(request, 'Votre paiement a bien été envoyé')


        if request.GET.get('p') == 'failure':
            messages.success(request, 'Vous n\'avez pas complété votre paiement. Veuillez réessayer')

    return render(request, 'accounts/dashboard.html')


