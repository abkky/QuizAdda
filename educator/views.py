from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,"eindex.html")
    else:
        return redirect("login")
def login(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user= auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect("/educator")
        else:
            messages.info(request,"Invalid Credentials")
            return redirect("login")
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
            return redirect("login")
        return redirect("/")
    else:
        return render(request,"signup.html")
def logout(request):
    auth.logout(request)
    return redirect("/")
def createquiz(request):
    return render(request,"createquiz.html")


def updateprofile(request):
  if request.method == 'POST':
        rename=request.POST["rename"]
        email=request.POST["uemail"]
        firstname=request.POST["ufirstname"]
        lastname=request.POST["ulastname"]        
        uid=request.POST["uid"]
        password=request.POST["upassword"]
        if User.objects.filter(username=rename).exists():
            messages.info(request,"Username is already taken")
            return redirect("updateprofile")
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email already exist")
            return redirect("updateprofile")
        else:
            user= User(id=uid,username=rename,password=password,email=email,first_name=firstname,last_name=lastname)
            user.save()
            return redirect("/educator/userprofile")
  else:
        return render(request,"updateprofile.html")
    
def userprofile(request):
    return render(request,"userprofile.html")

def updatepassword(request):
  if request.method == 'POST':
        rename=request.POST["username"]
        email=request.POST["uemail"]
        firstname=request.POST["ufirstname"]
        lastname=request.POST["ulastname"]        
        uid=request.POST["uid"]
        npassword=request.POST["npassword"]
        cpassword=request.POST["cpassword"]
        
       
        if npassword!=cpassword:
            messages.info(request,"new password not match")
            return redirect("updatepassword")
        else:
            user= User(id=uid,username=rename,password=cpassword,email=email,first_name=firstname,last_name=lastname)
            user.save()
            messages.info(request,"Password saved")
            return redirect("/educator/updatepassword")
  else:
        return render(request,"updatepassword.html")
    