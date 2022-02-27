from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect
from .models import Questions,Answer,Subject,TestName
from.forms import AddQFrm
from accounts.models import User
from io import BytesIO
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def exam_admin_home(request):
    return render(request,'exam_admin_home.html')

@staff_member_required
def new_question(request):
    msg=""
    if request.method=="POST":
        frm=AddQFrm(request.POST or None)
        if frm.is_valid():
            a=frm.save()
            if a:
                msg="Question Added Successfully"
    frm=AddQFrm()
    context={
        'frm':frm,
        'msg':msg,
    }
    return render(request,'add_question.html',context)

@staff_member_required
def view_question(request):
    qts=Questions.objects.all()
    context={
        'qts':qts,
    }
    return render(request,'view_questions.html',context)

@staff_member_required
def edit_questions(request,qid):
    qi=Questions.objects.get(id=qid)
    if request.method=='POST':
        frm=AddQFrm(request.POST,instance=qi)
        if frm.is_valid():
            frm.save()
            return redirect('view_question')
    frm=AddQFrm(instance=qi)
    context={
        'frm':frm,
    }
    return render(request,'add_question.html',context)

@staff_member_required
def delete_questions(request,qid):
    Questions.objects.filter(id=qid).delete()
    return redirect('view_question')

@staff_member_required
def students(request):
    students=User.objects.filter(is_staff=False,is_admin=False)
    context={
        'stds':students
    }
    return render(request,'student_list.html',context)

@staff_member_required
def answerd_questions(request,stdid):
    ans=Answer.objects.filter(student=stdid)
    context={
        'ans':ans
    }
    return render(request,'answers.html',context)

@staff_member_required
def result(request,stdid):
    subject=Subject.objects.all()
    testname=TestName.objects.all()
    qts=Answer.objects.filter(student=stdid)
   
    exam=[]
    i=0
    m=0
    for c in subject:
        
        for p in testname:
            ex={}
            q=qts.filter(question__subject=c.id,question__testname=p.id)
            an=[]
            for a in q:
                if a.answer==a.question.answers:
                    m=m+1
            if q:
                ex['total_marks']=30
                ex['marks']=m
                ex['answers']=q
                ex['subject']=c.subject
                ex['testname']=p.testname
                exam.append(ex)
               
            m=0
            i=i+1


    context={
        'exams':exam,
    }
    return render(request,'result.html',context)

@staff_member_required
def view_results(request):
    testname=TestName.objects.all()
    students=User.objects.filter(is_staff=False,is_admin=False)
    data=[]
    for student in students:
        std={}
        exams=Answer.objects.filter(student=student)
        std['student']=student
        pp=[]
        for p in testname:
            m=0
            for q in exams:
                if q.question.testname==p and q.answer==q.question.answers:
                    m=m+1
            pp.append(m)
            std['testname']=pp
        no_of_tests=len(pp)
        data.append(std)
    context={
        'datas':data,
        'total_tests':range(0,no_of_tests)
    }
    return render(request,'view_results.html',context)