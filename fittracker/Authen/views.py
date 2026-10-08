from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

# Create your views here.

def about(request):
    return render(request, 'about.html')

def register(request):
    if request.method == 'POST':
        fname = request.POST['fname'].strip()
        lname = request.POST['lname'].strip()
        email = request.POST['email'].strip()
        username = request.POST['username'].strip()
        password = request.POST['password']

        error = None
        if not username or not email or not password:
            error = 'Username, email and password are required.'
        elif User.objects.filter(username__iexact=username).exists():
            error = 'This username already exists.'
        elif User.objects.filter(email__iexact=email).exists():
            error = 'An account with this email already exists.'
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                error = ' '.join(e.messages)
        if error:
            return render(request, 'register.html', {'error': error,'form': {'fname': fname,'lname': lname,'email': email,'username': username,},})
        User.objects.create_user(
            username=username, email=email, password=password,
            first_name=fname, last_name=lname,
        )
        return redirect('login_')
    return render(request, 'register.html')

@login_required(login_url='login_')
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        username = request.POST['username'].strip()
        first_name = request.POST['first_name'].strip()
        last_name = request.POST['last_name'].strip()
        email = request.POST['email'].strip()
        if User.objects.filter(username__iexact=username).exclude(id=user.id).exists():
            return render(request, 'update_profile.html', {
                'error': 'This username is already taken.',
                'form': request.POST,
            })
        if User.objects.filter(email__iexact=email).exclude(id=user.id).exists():
            return render(request, 'update_profile.html', {
                'error': 'This email is already used by another account.',
                'form': request.POST,
            })
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        return redirect('profile')
    return render(request, 'update_profile.html', {'form': {'username': user.username,'first_name': user.first_name,'last_name': user.last_name,'email': user.email,}})

def login_(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        u = authenticate(username=username,password=password)
        if u:
            login(request, u)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Incorrect username or password'})
    return render(request, 'login.html')

@login_required(login_url='login_')
def profile(request):
    return render(request, 'profile.html')


@login_required(login_url='login_')
def logout_(request):
    logout(request)
    return redirect('login_')


@login_required(login_url='login_')
def reset_pass(request):
    user = request.user

    if request.method == 'POST':
        if 'old_pass' in request.POST:
            old = request.POST['old_pass']

            u = authenticate(
                username=user.username,
                password=old
            )

            if u:
                return render(request, 'reset.html', {
                    'new_pass': True
                })
            else:
                return render(request, 'reset.html', {
                    'error': 'Old password is incorrect'
                })

        if 'new_pass' in request.POST:
            new = request.POST['new_pass']

            user.set_password(new)
            user.save()

            return redirect('login_')

    return render(request, 'reset.html')

def forgot_pass(request):
    if request.method == 'POST':
        username = request.POST['username']
        try:
            u = User.objects.get(username=username)
            request.session['fp_user'] = u.username
            return redirect('new_password')
        except:
            return render(request,'forgot_pass.html',{'error':'Invalid Username'})
    return render(request,'forgot_pass.html')
 
def new_password(request):
    username = request.session.get('fp_user')
    if username is None:
        return redirect('forgot_pass')
    user = User.objects.get(username=username)
    if request.method == 'POST':
        new_pass = request.POST['new']
        if user.check_password(new_pass):
            return render(request,'new_pass.html',{'error':'New Password should not be same as old password'})
        user.set_password(new_pass)
        user.save()
        del request.session['fp_user']
        return redirect('login_')
    return render(request,'new_pass.html')