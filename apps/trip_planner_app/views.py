from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import datetime
from apps.login_app.models import User, UserManager, Trip, TripManager

def dashboard(request):
    if 'id' in request.session:
        user = User.objects.get(id=request.session['id'])
        user_trips = Trip.objects.filter(owner=user.id)
        
        tmp_trips = Trip.objects.filter(users=user)
        join_trips = tmp_trips.exclude(owner=user.id)
        
        others_trips_tmp = Trip.objects.exclude(users=user)
        others_trips= others_trips_tmp.exclude(owner=user.id)
        context={
            "user_trips": user_trips,
            "join_trips": join_trips,
            "others_trips": others_trips,
        }
        return render(request, "trip_planner_app/dashboard.html",context)
    else:
        return redirect('/')
    # return render(request, "trip_planner_app/dashboard.html")

def new_item(request):

    return render(request, "trip_planner_app/trip_add.html")
    # return HttpResponse("Add a new trip here")

def join_trip(request, id):
    t = Trip.objects.get(id=id)
    if 'id' in request.session:
        u = User.objects.get(id=request.session['id'])
        t.users.add(u)
    return redirect('/trips/dashboard')

def cancel_trip(request, id):
    t = Trip.objects.get(id=id)
    if 'id' in request.session:
        u = User.objects.get(id=request.session['id'])
        t.users.remove(u)
    return redirect('/trips/dashboard')


def create_item(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        if 'id' in request.session:
            dest = request.POST['dest']
            owner = request.session['id']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            plan = request.POST['plan']
            Trip.objects.create(dest=dest, owner=owner, start_date=start_date, end_date=end_date, plan=plan)
            # s = Show.objects.last()
            # id = s.id
            return redirect('/trips/dashboard')
        else:
            return redirect('/')
    # return HttpResponse("Create a new trip here")

def show_item(request, id):
    return redirect('/trips/'+str(id))

def show_info(request, id):
    trip = Trip.objects.get(id=id)
    users_tmp = User.objects.filter(trips=trip)
    users = users_tmp.exclude(id=trip.owner)
    context = {
        "trip": trip,
        "users": users,
    }
    return render(request, "trip_planner_app/trip_info.html", context)
    # return HttpResponse(f"Trip #{id} info here")

def edit_item(request, id):
    t = Trip.objects.get(id=id)
    if 'id' in request.session and t.owner == request.session['id']:
        trip = Trip.objects.get(id=id)
        context = {
            "trip": trip,
        }
        return render(request, 'trip_planner_app/trip_edit.html', context)
    else:
        redirect('/')
    # return HttpResponse(f"Edit item #{id} here")

def update_item(request, id):
    t = Trip.objects.get(id=id)
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/edit/'+str(id))
    else:
        t.owner = request.session['id']
        t.dest = request.POST['dest']
        t.user = User.objects.get(id=request.session['id'])
        t.start_date = request.POST['start_date']
        t.end_date = request.POST['end_date']
        t.plan = request.POST['plan']
        t.save()
        return redirect('/trips/dashboard')
    # return HttpResponse(f"Update item #{id} here")

def delete_item(request, id):
    t = Trip.objects.get(id=id)
    if 'id' in request.session and t.owner == request.session['id']:
        t = Trip.objects.get(id=id)
        t.delete()
        return redirect('/trips/dashboard')
    else:
        return redirect('/')  
    # return HttpResponse(f"Destroy item #{id} here")


def logout(request):
    if 'id' in request.session: 
        del request.session['id']
    if 'name' in request.session:
        del request.session['name']
    return redirect('/')
# def post_message(request):
    