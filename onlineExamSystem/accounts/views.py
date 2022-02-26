from django.shortcuts import render,redirect
from.forms import RegistrationForm,LoginForm,ExamChoiceFrm,AnsChoice
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt
from admin_dash.models import Questions,Subject,TestName,Answer
from django.contrib.auth import(
	authenticate,
	get_user_model,
	login as dj_login,
	logout

	)
from django.core import serializers

# Create your views here.

def register(request):
    if request.method=="POST":
        form=RegistrationForm(request.POST or None)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
       
            user=form.save(commit=False)
            
            user.set_password(password)
            user.save()
            newuser=authenticate(username=username,password=password)
           
            dj_login(request , newuser)
            return redirect(student_home)
       
    form=RegistrationForm()
    context={
        'form':form
    }

    return render(request,'std_register.html',context )

def login(request):
    if request.method=='POST':
        form=LoginForm(request.POST or None)
        if form.is_valid():
            password=form.cleaned_data.get('password')
            username=form.cleaned_data.get('username')
            user=authenticate(username=username,password=password)
            dj_login(request,user)
            return redirect(student_home)
    else:

        form=LoginForm()
        context={
        'form':form
    }
    return render(request,'login.html', context)

    
@login_required
def student_home(request):
    if request.method=='POST':
        form=ExamChoiceFrm(request.POST or None)
        if form.is_valid():        
            subject=request.user.subject
            request.session['subject']=request.user.subject.id
            testname=TestName.objects.filter(testname=form.cleaned_data.get('testname'))[0]
            request.session['testname']=testname.id
            ex=Answer.objects.filter(student=request.user,question__subject=subject,question__testname=testname)
            if ex:
                exam=ex[0].question
                if subject==exam.subject and testname==exam.testname:
                    form=ExamChoiceFrm()
                    context={
                        'form':form,
                        'msg':'Exam Already Completed',
                    }
                    return render(request,'student_home.html',context)
            else:
                qs=Questions.objects.filter(subject=subject,testname=testname)
                if qs:
                    qs=qs[0].qs_no
                    return redirect('exam_home',qs)
                else:
                    form=ExamChoiceFrm()
                    context={
                        'form':form,
                        'msg':'No Question testname Found',
                    }
                    return render(request,'student_home.html',context)
   
    form=ExamChoiceFrm()
    msg=""
    context={
        'form':form,
        'msg':msg,
    }
    return render(request,'student_home.html',context)

def logout_view(request):
	logout(request)
	return redirect('/')
    

def exam_home(request,qno):
    testname=request.session['testname']
    subject=request.session['subject']
    qts=Questions.objects.filter(subject=subject,testname=testname)
    try:
        qs=qts.filter(qs_no=qno)[0]
    except:
        qs=qts.filter(qs_no=1)[0]
    getqs=Answer.objects.filter(question=qs,student=request.user)
    if getqs:
        ans=Answer.objects.get(question=qs,student=request.user)
        msg="You have already choosen Option"
        request.session['msg']=msg
        if request.method=='POST':
            form=AnsChoice(request.POST or None)
            if form.is_valid():
                ans=form.cleaned_data.get('ans')
                getans=Answer.objects.get(question=qs,student=request.user)
                getans.answer=ans
                getans.save()
                nqno=int(qno) + 1
                request.session['msg']="Ans Saved Sucessfully"
                return redirect('exam_home' ,nqno)
    else:
        ans=""   
        request.session['msg']=""
        if request.method=='POST':
            form=AnsChoice(request.POST or None)
            if form.is_valid():
                ans=form.cleaned_data.get('ans')
                ansqs=Answer(
                    student=request.user,
                    question=qs,
                    answer=ans
                )
                ansqs.save()
                nqno=int(qno) + 1
                request.session['msg']="Ans Saved Sucessfully"
                return redirect('exam_home' ,nqno)
    ansfrm=AnsChoice()
    context={

        'ansfrm':ansfrm,
        'questions':qts,
        'qs':qs,
        'answer':ans,
        }
    return render(request,'question.html',context)
