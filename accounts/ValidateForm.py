from django.contrib import messages, auth
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
import re

class ValidateForm:

    errors = []

    def __init__(self, request):
        self.request = request

    def register_form(self, first_name, last_name, email, username, password, password_conf):
        # firstname
        if not first_name:
            self.errors.append(messages.error(self.request, 'Le prénom ne doit pas être vide'))
            return False
        elif len(first_name) < 3:
            self.errors.append(messages.error(self.request, 'Le prénom doit être d\'au moins 3 caractères'))
            return False

        # lastname
        if not last_name:
            self.errors.append(messages.error(self.request, 'Le nom de famille ne doit pas être vide'))
            return False
        elif len(last_name) < 3:
            self.errors.append(messages.error(self.request, 'Le nom de famille doit être d\'au moins 3 caractères'))
            return False

        # email
        if not email:
            self.errors.append(messages.error(self.request, 'L\'adresse courriel doit être valide.'))
            return False
        elif re.match('\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', email) != None:
            self.errors.append(messages.error(self.request, 'L\'adresse courriel doit être valide.'))
            return False
        elif User.objects.filter(email=email).exists():
            self.errors.append(messages.error(self.request, 'Désolé, ce courriel est déjà associé à un compte.'))
            return False

        # username
        if not username:
            self.errors.append(messages.error(self.request, 'L\'identifiant ne doit pas être vide'))
            return False
        elif len(username) < 5:
            self.errors.append(messages.error(self.request, 'L\'identifiant doit être d\'au moins 5 caractères'))
            return False
        elif User.objects.filter(username=username).exists():
            self.errors.append(messages.error(self.request, 'Désolé, cet identifiant est déjà associé à un compte.'))
            return False

        # password
        if not password:
            self.errors.append(messages.error(self.request, 'Le mot de passe ne doit pas être vide.'))
            return False
        elif len(password) < 8:
            self.errors.append(messages.error(self.request, 'Le mot de passe doit être d\'au moins 8 caractères'))
            return False

        # password conf
        if password_conf != password:
            self.errors.append(messages.error(self.request, 'La confirmation du mot de passe doit être identique au mot de passe'))
            return False
        else:
            return True

    def get_error_messages(self):
        for error in self.errors:
            return error
