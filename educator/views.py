from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth


# Create your views here.
def index(request):
    return render(request,"eindex.html")
def login(request):
    if request.method == 'POST':
        pass
    else:
        return render(request,"login.html")
def signup(request):
    if request.method == 'POST':
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        email=request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        if User.objects.filter(username=username).exists():
            messages.info(request,"Username is already taken")
            return redirect("signup")
        elif User.objects.filter(email=email):
            messages.info(request,"Email already exist")
            return redirect("signup")
        else:
            user= User.objects.create_user(username=username,password=password,email=email,first_name=firstname,last_name=lastname)
            user.save()
            print('User Created')
        return redirect("/")
    else:
        return render(request,"signup.html")