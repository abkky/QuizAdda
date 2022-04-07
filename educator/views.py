from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import answers, question, quiz,responser
import datetime


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return render(request,"eindex.html")
    else:
        return redirect("login")
def validateusername(request):
    if request.method == 'POST':
        username=request.POST["username"]
        if User.objects.filter(username__iexact=username.lower()).exists():
            return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':1})
def validateemail(request):
    if request.method == 'POST':
        email=request.POST["email"]
        if User.objects.filter(email__iexact=email.lower()).exists():
            return JsonResponse({'status':0})
        else:
            return JsonResponse({'status':1})
def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST["username"]
            password = request.POST["password"]
            user= auth.authenticate(username=username.lower(),password=password.lower())
            if user is not None:
                auth.login(request,user)
                return redirect("/educator")
            else:
                messages.info(request,"Invalid Credentials")
                return redirect("login")
        else:
            return render(request,"login.html")
    else:
        return redirect("/educator")
def signup(request):
    if request.method == 'POST':
        firstname=request.POST["firstname"]
        lastname=request.POST["lastname"]
        email=request.POST["email"]
        email=email.lower()
        username=request.POST["username"]
        username=username.lower()
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
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect("/")
    else:
        return redirect("login")
def createquiz(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            uid=request.POST["userid"]
            quizname=request.POST["quizname"]
            quizdesc=request.POST["quizdesc"]
            quiz_save=quiz(uid=uid,quizname=quizname,quizdesc=quizdesc,quizstatus=False,creationdate=datetime.datetime.now().strftime ("%Y-%m-%d"),creationtime=datetime.datetime.now().strftime ("%H:%M"))
            quiz_save.save()
            obj = quiz.objects.filter(uid=uid).latest('id')
            request.session['qid'] = obj.id
            return redirect("/educator/createquestion")
        else:    
            return render(request,"createquiz.html")
    else:
        return redirect("login")
def createquestion(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            try:
                quizidfe=request.POST["quizidfe"]
                questionin=request.POST["question"]
                numofques=request.POST["numofquestion"]
                correctoption=request.POST["co"]
                option1=request.POST["ov1"]
                option2=request.POST["ov2"]
                try:
                    option3=request.POST["ov3"]
                except:
                    option3=""
                try:
                    option4=request.POST["ov4"]
                except:
                    option4=""
                try:
                    option5=request.POST["ov5"]
                except:
                    option5=""
                ques_save=question(quizid=quizidfe,question=questionin,numofques=numofques,correctoption=correctoption,option1=option1,option2=option2,option3=option3,option4=option4,option5=option5)
                ques_save.save()
                return redirect("/educator/createquestion")
            except:
                return HttpResponse('<script type="text/javascript"> alert("Please fill the form properly"); window.location.href = "/educator/createquestion";</script>;')
    
        else:
            # try:
                qid=request.session['qid']
                quizdb=quiz.objects.get(id=qid)
                fequiz=reversed(question.objects.filter(quizid=qid))
                quesnums=len(question.objects.filter(quizid=qid))
                context={"id":qid,"quizquesall":fequiz,"quesnums":quesnums,"quiz":quizdb}
                return render(request,"createquestion.html",context)
            # except:
            #     return HttpResponse ('<script type="text/javascript"> alert("Please Create a Quiz first"); window.location.href = "/educator/createquiz";</script>;')
    else:
        return redirect("login")

def updateprofile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            firstname=request.POST["firstname"]
            lastname=request.POST["lastname"]
            username=request.POST["username"]
            u1=request.user      
            if u1.username!=username:
                if User.objects.filter(username=username).exists():
                    messages.info(request,"Username is already taken")
                    return redirect("/educator/updateprofile")
                else:
                    User.objects.filter(id=u1.id).update(first_name=firstname,last_name=lastname,username=username.lower())
                    return redirect("/educator/userprofile")
            else:
                User.objects.filter(id=u1.id).update(first_name=firstname,last_name=lastname)
                return redirect("/educator/userprofile")
        else:
            return render(request,"updateprofile.html")
    else:
        return redirect("login")
    
def userprofile(request):
    if request.user.is_authenticated:
        return render(request,"userprofile.html")
    else:
        return redirect("login")

def updatepassword(request):
    if request.user.is_authenticated:
        if request.method == 'POST':    
                uid=request.user
                uid=uid.id
                npassword=request.POST["npassword"]
                cpassword=request.POST["cpassword"]
                if npassword!=cpassword:
                    messages.info(request,"Password not matched")
                    return redirect("/educator/updatepassword")
                else:
                    user= User.objects.get(id=uid)
                    user.set_password(npassword)
                    user.save()
                    messages.info(request,"Password Updated")
                    return redirect("/educator/updatepassword")
        else:
                return render(request,"updatepassword.html")
    else:
        return redirect("login")
    
def publishquiz(request):
    if request.method == "POST":
        qid=request.POST['quizidfe']
        fr = quiz.objects.get(id = qid)
        fr.quizstatus = True
        fr.save()
        try:
            del request.session['qid']
        except  KeyError:
             pass
        return JsonResponse({'status':'Quiz Saved, will be published on provided time'})
        
    else:
        return JsonResponse({'status':0})
def quizzes(request):
    if request.user.is_authenticated:
        uid = request.user.id
        fequiz=quiz.objects.filter(uid=uid)
        numofquiz=len(quiz.objects.filter(uid=uid))
        context={"allquizuser":fequiz,"numofquizzes":numofquiz}
        return render(request,"quizzes.html",context)
    else:
        return redirect("login")
def viewquiz(request):
    if request.user.is_authenticated:
        try:
            try:
                quizidfe=request.POST['quizidfe']
            except:
                quizidfe=request.session['quizidtemp']
            request.session['qid'] = quizidfe
            fequiz2=question.objects.filter(quizid=quizidfe)
            fequizdet=quiz.objects.get(id=quizidfe)
            numofques=len(question.objects.filter(quizid=quizidfe))
            context={"quizquesall":fequiz2,"numofques":numofques,"fequizdet":fequizdet,"quizid":quizidfe}
            return render(request,"viewquiz.html",context)
        except:
            return HttpResponse('<script type="text/javascript"> alert("Do not try to act smart, go and check a quiz first"); window.location.href = "/educator/quizzes";</script>;')
    else:
        return redirect("login")
def quizmodify(request):
    if request.user.is_authenticated:
        quizidfe=request.POST["quizidfe"]
        quizvv=quiz.objects.get(id=quizidfe)
        context={"quiz":quizvv}
        return render(request,"modifyquiz.html",context)
        
    else:
        return redirect("login")

def deletequiz(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            qid=request.POST["quizidfe"]
            question.objects.filter(quizid=qid).delete()
            quiz.objects.filter(id=qid).delete()
            return HttpResponse('<script type="text/javascript"> alert("Quiz deleted"); window.location.href = "/educator/quizzes";</script>;')
            
    else:
        return redirect("login")
def deleteques(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            qid=request.POST["quesidfe"]
            quizidfe=request.POST["quizidfe"]
            request.session['quizidtemp']=quizidfe
            question.objects.filter(id=qid).delete()
            return HttpResponse('<script type="text/javascript"> alert("Question deleted"); window.location.href = "/educator/viewquiz";</script>;')
                
    else:
        return redirect("login")
def updatequiz(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            qid=request.POST["quizidfe"]
            quizname=request.POST["quizname"]
            quizdesc=request.POST["quizdesc"]
            statustext=request.POST["status"]
            if statustext == "Accepting":
                status=True
            else:
                status=False
            quiz.objects.filter(id=qid).update(quizname=quizname, quizdesc=quizdesc,quizstatus=status)
            return HttpResponse('<script type="text/javascript"> alert("Quiz Updated"); window.location.href = "/educator/quizzes";</script>;')
            
    else:
        return redirect("login")
def analytics(request):
    if request.user.is_authenticated:
        uid=request.user.id
        quizs=reversed(quiz.objects.filter(uid=uid))
        numofq=len(quiz.objects.filter(uid=uid))
        context={"quizfe":quizs, "numofq":numofq}
        return render(request,"analytics.html",context)
    else:
        return redirect("login")
def anquiz(request,qid):
    if request.user.is_authenticated:
        uid=request.user.id
        if quiz.objects.filter(id=qid,uid=uid).exists():
            q=quiz.objects.get(id=qid)
            numofqq=len(question.objects.filter(quizid=qid))
            res=responser.objects.filter(quizid=qid, substatus=True)
            numofr=len(res)
            context={"quiz":q,"rees":res,"numofr":numofr,"numofq":numofqq}
            return render(request,"anquiz.html",context)
        else:
            return HttpResponse('<script type="text/javascript"> alert("Invalid Access"); window.location.href = "/educator/analytics";</script>;')
    else:
        return redirect("login")
def squiz(request,qid,uid):
    if request.user.is_authenticated:
        usrid=request.user.id
        if quiz.objects.filter(id=qid,uid=usrid).exists():
            quizfe=quiz.objects.get(id=qid)
            ques=question.objects.filter(quizid=qid)
            res=responser.objects.get(id=uid)
            ans=answers.objects.filter(uid=uid)
            context={"quiz":quizfe,"questions":ques,"res":res,"answers":ans}
            return render(request,"squiz.html",context)
        else:
            return HttpResponse('<script type="text/javascript"> alert("Invalid Access"); window.location.href = "/educator/analytics";</script>;')
    else:
        return redirect("login")