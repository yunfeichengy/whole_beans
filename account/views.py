from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User                     # user model !
from django.contrib.auth import authenticate, login, logout     # for user authentication
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from . import forms

# python decorator
# specifies that this view only works if user is logged in
# if not, go to login url defined in whole_beans/settings and set this 'info' view as the next redirect
@login_required
def info(request):
    # once a user is logged in, can use !!!request.user!!! to get info about user, i.e. username attributes
    return HttpResponse('Hello ' + request.user.username)


def signup(request):
    context = {}
    if request.method == 'POST':
        # request.POST will contain the form data. use it to instantiate parameters of signupForm
        form = forms.SignupForm(request.POST)
        if form.is_valid():  # check all required fields are there. check their types too
            try:
                user = User.objects.create_user(  # can pass other user fields as well, returns a user model instance
                    form.cleaned_data['username'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password'])  # takes care of hashing password.
                # user is saved to database automatically.
                # redirect to login page, redirects via reverse() -> path
                return HttpResponseRedirect(reverse('login'))
            # this checks on the username to ensure not having the same usernames in the database
            except IntegrityError:
                form.add_error('username', 'Username is already taken.')

        # if failed, return form. so that what the user entered is not lost
        context['form'] = form
    return render(request, 'account/signup.html', context)


def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,  # will look for user with these username and password and return that user
                                username=form.cleaned_data['username'],
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)  # use session to store id of user
                # redirect paths
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('listAllproduct'))  # go to marketplace main page
            else:
                form.add_error(None, 'Unable to log in.')  # form.add_error, first param is None i.e. not field a specific error, second param message
        context['form'] = form
    return render(request, 'account/login.html', context)


def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
