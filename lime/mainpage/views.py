from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def signup_(request):
    error = None
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.data.get('password1') != form.data.get('password2'):
            error = 'گذرواژه و تکرار گذرواژه یکسان نیستند'
        if User.objects.filter(username=form.data.get('username')).exists():
            error = "کاربری با نام کاربری وارد شده وجود دارد"
        if User.objects.filter(email=form.data.get('email')).exists():
            error = 'کاربری با ایمیل وارد شده وجود دارد'

        if error is None and form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, email=form.data.get('email'), password=raw_password)
            user.first_name = form.data.get('name')
            user.last_name = form.data.get('family')
            user.save()

            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('/home')

    return render(request, 'sign_up.html', {'error': error})


def login_(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/home")
        return render(request, "login_form.html", {"error": True})
    return render(request, "login_form.html")


def logout_(request):
    logout(request)
    return HttpResponseRedirect("/home")


def home(request):
    return render(request, 'home.html', {'isLoggedIn': (request.user is not None)})


@login_required(login_url="/login")
def user_profile(request):
    return render(request, """user_profile""")


@login_required(login_url="/login")
def edit_profile1(request):
    return render(request, """user_profile1""")


@login_required(login_url="/login")
def edit_profile2(request):
    return render(request, """user_profile2""")
