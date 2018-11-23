from IPython.core.display import display_markdown
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from mainpage.models import UserProfile
from markdown import markdown


def signup_(request):
    error = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.data.get('password1') != form.data.get('password2'):
            error = 'گذرواژه و تکرار گذرواژه یکسان نیستند'
        if User.objects.filter(username=form.data.get('username')).exists():
            error = "کاربری با نام کاربری وارد شده وجود دارد"
        if User.objects.filter(email=form.data.get('email')).exists():
            error = 'کاربری با ایمیل وارد شده وجود دارد'

        if error is '' and form.is_valid():
            if not Group.objects.filter(name='student').exists():
                group = Group(name='student')
                group.save()
            else:
                group = Group.objects.get(name='student')
            if 'professor' in form.data.get('type'):
                if not Group.objects.filter(name='professor').exists():
                    group = Group(name='professor')
                    group.save()
                else:
                    group = Group.objects.get(name='professor')

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = User.objects.create_user(username, email=form.data.get('email'), password=raw_password)
            user.first_name = form.data.get('name')
            user.last_name = form.data.get('family')
            user.groups.add(group)
            user.save()
            user_profile = UserProfile.objects.get_or_create(user=user, gender='F')

            user = authenticate(username=username, password=raw_password)

            login(request, user)
            return redirect('/')

    return render(request, 'sign_up.html', {'error': error})


def login_(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect("/home")
        return render(request, "login_form.html", {"error": 'نام کاربری یا گذرواژه غلط است'})
    return render(request, "login_form.html")


def logout_(request):
    logout(request)
    return render(request, "home.html", {"isLoggedIn": False})


def home(request, accept=0):
    # user = User.objects.filter(request.user).get()
    if request.user.id is not None:
        fname = request.user.first_name
        lname = request.user.last_name
        username = request.user.username
    else:
        fname = ''
        lname = ''
        username = ''
    if accept != 0:
        return render(request, 'home.html', {'message': 'درخواست شما ثبت شد',
                                             'isLoggedIn': (request.user.id is not None),
                                             'name': fname,
                                             'family': lname,
                                             'username': username
                                             })

    return render(request, 'home.html', {'isLoggedIn': (request.user.id is not None),
                                         'name': fname,
                                         'family': lname,
                                         'username': username})


@login_required(login_url="/login")
def user_profile(request):
    user = request.user
    gender = 'مرد'
    bio = ''
    picture = ''
    group = 'استاد'
    if user.groups.filter(name='student').exists():
        group = 'دانشجو'

    if (UserProfile.objects.filter(user=user).exists()):
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.gender is 'F':
            gender = 'زن'
        bio = user_profile.bio
        bio = markdown(bio)
        # if user_profile.picture is not None :
        picture = user_profile.image_tag()

    return render(request, "profile.html",
                  {"username": user.username,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   'gender': gender,
                   "bio": bio,
                   'picture': picture,
                   'group': group,
                   })


@login_required(login_url="/login")
def change(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        # if form.is_valid():
        username = request.user.username
        user = User.objects.get(username=username)
        # if form.data.get('name') is not '':
        user.first_name = form.data.get('name')
        user.last_name = form.data.get('lastname')
        user.save()
        if (UserProfile.objects.filter(user=user).exists()):
            user_profile = UserProfile.objects.get(user=user)
            user_profile.bio = form.data.get('bio')
            user_profile.gender = form.data.get('gender')
            if len(request.FILES) is not 0:
                user_profile.picture = request.FILES['picture']
            user_profile.save()

        return HttpResponseRedirect('/profile')
    return render(request, 'editProf.html')


#
# @login_required(login_url="/login")
# def change(request):
#     return render(request, 'editProf.html')


def contact(request):
    if request.method == 'POST':
        error = ''
        form = UserCreationForm(request.POST)
        text = form.data.get('text')
        title = form.data.get('title')
        email = form.data.get('email')
        if text is '' or title is '':
            error = 'فیلد های اجباری را پر کنید'
            return render(request, 'ContactUs.html', {
                'error': error
            })
        if len(text) < 10 or len(text) > 250:
            error = 'طول متن استاندارد نیست'
            return render(request, 'ContactUs.html', {
                'error': error
            })
        email = EmailMessage(title, 'opinion: ' + text + '\nemail: ' + email, to=['ostadju@fastmail.com'])
        email.send()
        # send_mail(
        #     title,
        #     text + email,
        #     '0.0.0.0:8000',
        #     ['ostadju@fastmail.com'],
        #     fail_silently=False,
        # )
        return HttpResponseRedirect('/home/1')
    return render(request, 'ContactUs.html')


def search(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        users_in_group = Group.objects.get(name="professor").user_set.all()
        """CHECK IT!!!!"""
        # if form.is_valid():
        phrase = form.data.get('phrase')
        if phrase is '':
            return HttpResponseRedirect("")

        profs = users_in_group.filter(first_name__contains=phrase) | users_in_group.filter(last_name__contains=phrase) | users_in_group.filter(username__contains=phrase)

        return render(request, 'search_result.html', {'profs': profs})
    return HttpResponseRedirect("")


def markdown(request):
    pass


def get_profile(request, username):
    user = User.objects.get(username=username)
    gender = 'مرد'
    bio = ''
    picture = ''
    group = 'استاد'
    if user.groups.filter(name='student').exists():
        group = 'دانشجو'

    if (UserProfile.objects.filter(user=user).exists()):
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.gender is 'F':
            gender = 'زن'
        bio = user_profile.bio
        picture = user_profile.image_tag()

    return render(request, "profile.html",
                  {"username": user.username,
                   "first_name": user.first_name,
                   "last_name": user.last_name,
                   'gender': gender,
                   "bio": bio,
                   'picture': picture,
                   'group': group,
                   })

