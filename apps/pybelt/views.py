from django.shortcuts import render, HttpResponse, redirect
from . models import *
from django.contrib import messages

def index(request):
	return render (request, "pybelt/index.html")

def register(request):
	if request.method =='POST':
		errors = User.objects.registration_validator(request.POST)
		if (type(errors) == dict and len(errors) != 0):
			for key,error_val in errors.items():
				messages.error(request, error_val)
			return redirect('/main')
		result = User.objects.create(name = request.POST['name'], username = request.POST['username'], password = errors)
		request.session['user_id'] = result.id
	return redirect ('/travels')


def login(request):
	if request.method == "POST":
		user = User.objects.login_validator(request.POST)
		if (type(user) == dict and len(user)!=0):
			for key, error_val in user.items():
				messages.error(request, error_val)
			return redirect('/main')
		request.session['user_id'] = user.id
	return redirect('/travels')

def travels(request):
	if 'user_id' not in request.session:
		return redirect('/main')

	user = User.objects.get(id= request.session['user_id'])
	trips = Trip.objects.all().exclude(users= user)
	joinTrips = Trip.objects.all().filter(users= user)

	context = {	
	'user' : user,
	'trips' : trips,
	'joinTrips': joinTrips
	}
	
	return render (request, 'pybelt/list.html', context)



def addtrip(request):
	if 'user_id' not in request.session:
		return redirect('/main')
	
	return render(request, 'pybelt/add.html')




def add(request):
	if request.method =='POST':
		errors = Trip.objects.Travel_regi_validator(request.POST)
		if (type(errors) == dict and len(errors) != 0):
			for key,error_val in errors.items():
				messages.error(request, error_val)
			return redirect('/travels/add')

		
		result = Trip.objects.create(destination = request.POST['destination'], desc = request.POST['desc'], start_day = request.POST['start_day'], end_day = request.POST['end_day'], )
		print result

		trip = Trip.objects.last()
		user = User.objects.get(id=request.session['user_id'])
		user.travels.add(trip)
		
	return redirect ('/travels')


def join(request, id):
	if 'user_id' not in request.session:
		return redirect('/main')

	trip = Trip.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	user.travels.add(trip)
	
	return redirect('/travels')

def unjoin(request, id):
	if 'user_id' not in request.session:
		return redirect('/main')

	trip = Trip.objects.get(id=id)
	user = User.objects.get(id=request.session['user_id'])
	user.travels.remove(trip)

	# user = User.objects.get(id=request.session['user_id'])
	# message = Message.objects.get(id=id)
	# message.liked_users.remove(user) 

	return redirect('/travels')

def viewpage(request, id):
	if 'user_id' not in request.session:
		return redirect('/main')
	print "GO"

	user = User.objects.get(id= request.session['user_id'])
	trip = Trip.objects.get(id= id)
	other = User.objects.all().exclude(id = request.session['user_id'])
	other_users = trip.users.all()


	context = {
		'trip': trip,
		"other_users": other_users,
	}

	return render(request, 'pybelt/view.html', context)


def logout(request):
	if 'user_id' in request.session:
		del request.session['user_id']
	return redirect('/main')





# def deleteuser(request):
# 	User.objects.get(id=2).delete()
# 	return redirect('/travels')
