from django.shortcuts import render, HttpResponse, redirect
from .models import User, Trip

from django.contrib import messages
import bcrypt

def index(request):
    return render(request, "index.html")

def regUpdate(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password = request.POST["passwordLabel"]
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        created_user = User.objects.create(
            first_name = request.POST['firstNameLabel'],
            last_name = request.POST['lastNameLabel'],
            email = request.POST['emailLabel'],
            password = pw_hash
        )

        request.session['userId'] = created_user.id
        request.session['userName'] = created_user.first_name
        return redirect('/success')


def loginProcess(request):
    
    user = User.objects.filter(email=request.POST['emailLabel'])
    if len(user) == 0:
        messages.error(request, "Please check your email and password")
        return redirect("/")
    if bcrypt.checkpw(request.POST['passwordLabel'].encode(), user[0].password.encode()):
        request.session['userId'] = user[0].id
        request.session['userName'] = user[0].first_name
        return redirect("/success")
        
    else:
        messages.error(request, "Please check your email and password")
        return redirect("/")

def successView(request):
    if "userId" not in request.session:
        
        messages.error(request, "you are not logged in!!!")
        return redirect('/')
    else:
       # trips = Trip.objects.all()
        print('entering success page with trips')
        all_Trips = Trip.objects.all().order_by('start_date').reverse()
        context = {
            'all_trips': all_Trips
        }
        return render(request, "success.html", context)


def loggingOut(request):
    request.session.clear()
    return redirect("/")


def view_Trip(request, trip_id):
    context = {
         'this_user_trip' : Trip.objects.get(id=trip_id)
    }
    return render(request, "view-trip.html", context)


def delete_trip(request, trip_id):
    trip_to_delete = Trip.objects.get(id=trip_id)
    trip_to_delete.delete()

    return redirect ( "/success")


def updatingTrip(request, trip_id): #id3 coming from url:id3 
    errors = Trip.objects.basic_validator_two(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect(request.META.get('HTTP_REFERER')) #return an instance of HttpResponse to stay in same page

    else:
        updatedTrip = Trip.objects.get(id=trip_id)

        updatedTrip.destination = request.POST['destinationLabel']
        updatedTrip.startdate = request.POST['startDateLabel']
        updatedTrip.enddate = request.POST['endDateLabel']
        updatedTrip.plan = request.POST['planLabel']

        updatedTrip.save()

        return redirect (f"/trips/{updatedTrip.id}")



#passing selected trip into editing page
def edit_trip_page(request, trip_id): 
    #print("editing trip ")
    
    trip = Trip.objects.get(id=trip_id)
    context = {
        #'user' : userid
        'selected_trip': trip,
        # 'start' : trip.start_date.strftime("%Y-%m-%d")
    } #new code above
    return render(request, "edit_trip.html", context)
    #render only renders file.html


def edit_trip_process(request, trip_id):
    
    errors = Trip.objects.basic_validator_two(request.POST)
    
    if len(errors) > 0:
        for key, value in errors.items():
            #by calling the error function
            #we'll have acces to the erros we set
            # on the next request
            messages.error(request, value)
        # redirect the user back to the form to fix the errors 
        #this is prompting another request
        return redirect(request.META.get('HTTP_REFERER'))
    else:

        current_trip = Trip.objects.get(id=trip_id)
        current_trip.destination = request.POST['destinationLabel']
        current_trip.start_date = request.POST['startDateLabel']
        current_trip.end_date = request.POST['endDateLabel']
        current_trip.plan = request.POST['planLabel']
        #current_trip.owner = User.objects.get(id=request.session['userId'])
        owner = User.objects.get(id=request.session['userId'])
        current_trip.save()

        return redirect('/success')


    
def realAddingTrip(request):
    
    errors = Trip.objects.basic_validator_two(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            #by calling the error function
            #we'll have acces to the erros we set
            # on the next request
            messages.error(request, value)
        # redirect the user back to the form to fix the errors 
        #this is prompting another request
        return redirect('/trip/new')

    else:
        Trip.objects.create(
        destination = request.POST['destinationLabel'],
        start_date = request.POST['startDateLabel'],
        end_date = request.POST['endDateLabel'],
        plan = request.POST['planLabel'],
        owner = User.objects.get(id=request.session['userId'])
    )

    return redirect('/success')


def addingTrip(request):
    return render(request, "new.html")

