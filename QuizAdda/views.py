import datetime
from django.shortcuts import redirect, render,HttpResponse
from educator.models import quiz,question,responser,answers
from django.contrib.auth.models import User
from django.http import HttpRequest  
# Create your views here.
def index(request):
    numofquiz=len(quiz.objects.all())
    numofques=len(question.objects.all())
    creators=len(User.objects.all())
    context={"numofquiz":numofquiz,"numofques":numofques,"creators":creators}
    return render(request,"index.html",context)
def joinquiz(request,id):
    if quiz.objects.filter(id=id).exists():
        quizfe=quiz.objects.get(id=id)
        if quizfe.quizstatus is True:
            if request.method=="POST":
                quizid=quizfe.id
                name=request.POST["name"]
                email=request.POST["email"]
                if responser.objects.filter(email=email,quizid=quizid).exists() :
                    status=responser.objects.get(email=email)
                    uid=status.id
                    status=status.substatus
                    if status is True:
                        return HttpResponse('<script type="text/javascript"> alert("You have already submitted quiz."); window.location.href = "/";</script>;')
                    else:
                        responser.objects.filter(id=uid).update(subdate=datetime.datetime.now().strftime ("%Y-%m-%d"),subtime=datetime.datetime.now().strftime ("%H:%M"))
                        obj = responser.objects.filter(quizid=quizid,email=email).latest('id')
                        request.session['uid'] = obj.id
                        request.session["tqid"]=quizid
                        return redirect("/attemptquiz")
                else:
                    res=responser(quizid=quizid,name=name,email=email,subdate=datetime.datetime.now().strftime ("%Y-%m-%d"),subtime=datetime.datetime.now().strftime ("%H:%M"))
                    res.save()
                    obj = responser.objects.filter(quizid=quizid,name=name,email=email).latest('id')
                    request.session['uid'] = obj.id
                    request.session["tqid"]=quizid
                    return redirect("/attemptquiz")
            else:
                usr=User.objects.get(id=quizfe.uid)            
                context={"quiz":quizfe,"usr":usr}
                return render(request,"joinquiz.html",context)
        else:
            return HttpResponse('<script type="text/javascript"> alert("Educator is not accepting responses now."); window.location.href = "/";</script>;')
    else:
        return HttpResponse('<script type="text/javascript"> alert("Invalid Quiz ID"); window.location.href = "/";</script>;')
def tjoin(request):
    if request.method=="POST":
        qid=request.POST["quizid"]
        if quiz.objects.filter(id=qid).exists():
            url="/joinquiz/"+qid
            return redirect(url)
        else:
            return HttpResponse('<script type="text/javascript"> alert("Invalid Quiz ID"); window.location.href = "/";</script>;')
def attemptquiz(request):
    try:
        quizid=request.session['tqid']
        uid=request.session['uid']
        quizmain=question.objects.filter(quizid=quizid)
        quizdet=quiz.objects.get(id=quizid)
        muid=quizdet.uid
        usr=User.objects.get(id=muid)
        res=responser.objects.get(id=uid)
        context={"questions":quizmain,"quiz":quizdet,"res":res,"usr":usr}
        if request.method=="POST":
            if quizdet.quizstatus == True:

                pre="option"
                for i in range(1,len(quizmain)+1):
                    x=pre+str(i)
                    ov=request.POST[x]
                    quesid=quizmain[i-1].id
                    save_response=answers(uid=uid,quesid=quesid,option=ov)
                    save_response.save()
                    correctop=question.objects.get(id=quesid)
                    correctop=correctop.correctoption
                    if correctop==int(ov):
                        incrm=responser.objects.get(id=uid)
                        incrm.score += 1
                        incrm.save()
                responser.objects.filter(id=uid).update(substatus=True)
                incr=quiz.objects.get(id=quizid)
                print(incr.attempts)
                incr.attempts += 1
                incr.save()
                print(incr.attempts)

                try:
                    del request.session['tqid']
                except  KeyError:
                    pass
                return HttpResponse('<script type="text/javascript"> alert("Quiz Submitted"); window.location.href = "/";</script>;')
            else:
                try:
                    del request.session['tqid']
                except  KeyError:
                    pass
                return HttpResponse('<script type="text/javascript">alert("Response Closed"); window.location.href = "/";</script>;')
        else:
            return render(request,"attemptquiz.html",context)
    except:
         return HttpResponse('<script type="text/javascript"> alert("Invalid Access"); window.location.href = "/";</script>;')
