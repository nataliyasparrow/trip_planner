from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, UserManager, Trip, TripManager
import bcrypt

def index(request):
    if 'id' in request.session:
        return redirect('/trips/dashboard')
    return render (request, "login_app/index.html")
    # return HttpResponse("Login and registration will be here asap")

def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['fname']
        last_name = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pw']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        conf_password = request.POST['pw_conf']
        # request.session['email'] = email
        User.objects.create(first_name=first_name, last_name=last_name, email=email, password=pw_hash.decode())
        request.session['name'] = first_name
        request.session['id'] = User.objects.last().id
        return redirect('/trips/dashboard')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        # request.session["email"] = request.POST['l_email']
        u = User.objects.filter(email=request.POST['l_email'])
        request.session["name"] = u[0].first_name
        request.session["id"] = u[0].id
        return redirect('/trips/dashboard')

# def success(request):
#     if 'id' not in request.session:
#         return redirect('/')
#     else:
#         return render(request, "login_app/welcome.html")

def logout(request):
    if 'id' in request.session: 
        del request.session['id']
    if 'name' in request.session:
        del request.session['name']
    return redirect('/')