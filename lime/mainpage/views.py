from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect


# Create your views here.

def signup_(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home')
    else:
        form = UserCreationForm()
    return render(request, 'sign_up.html', {'form': form})


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
    return HttpResponseRedirect("/login")


def home(request):
    return render(request, 'home.html', {'isLogedIn': (request.user != None)})


@login_required(login_url="/login")
def user_profile(request):
    return render(request, """user_profile""")


@login_required(login_url="/login")
def edit_profile1(request):
    return render(request, """user_profile1""")


@login_required(login_url="/login")
def edit_profile2(request):
    return render(request, """user_profile2""")
