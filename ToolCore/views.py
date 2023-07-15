from django.shortcuts import render,redirect
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from .forms import PaperDetailForm
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import RequestContext
from django.views import View
import json

def home(request):
    return render(request,'ToolCore/homepage.html')

def loginPage(request):
    page='login'
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not Exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'User password is not Correct')
    context = {'page':page}
    return render(request,'ToolCore/login_register.html',context)

def registerPage(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error occured during registration')

    return render(request,'ToolCore/login_register.html')

def logoutUser(request):
    logout(request)
    return redirect('home')



def toolPage(request):
    class_response = requests.get('http://54.252.241.208/api/v1/classes/')
    # chapters = chapter_response.json()
    classes = class_response.json()
    
    if request.method == 'POST':
        form = PaperDetailForm(request.POST)
        # if form.is_valid():
            # form.save()
        text = request.POST.get('instructions')
        rows = text.split('\n')
        
        class_id = request.POST.get('class_name')
        subject_id = request.POST.get('subject_name')
        class_response = requests.get('http://54.252.241.208/api/v1/classes/' + class_id + '/')
        subject_response = requests.get('http://54.252.241.208/api/v1/subjects/' + subject_id + '/')
        class_name = class_response.json()['class_name']
        subject_name = subject_response.json()['subject_name']
        # context = {'class_name':class_name,'subject_name':subject_name,'form':form,'rows':rows,'chapters':chapters}
        request.session['class_name'] = class_name 
        request.session['subject_name'] = subject_name
        request.session['rows'] = rows 
        request.session['duration'] = request.POST.get('duration') 
        request.session['marks'] = request.POST.get('marks') 
        request.session['school_name'] = request.POST.get('school_name')
        request.session['exam_name'] = request.POST.get('exam_name')
        request.session['date'] = request.POST.get('date')
        request.session['subject_id'] = subject_id 
        return redirect('book-chapter')
        # return render(request,'paper_creation_tool/toolpage.html',context)
    else:
        form = PaperDetailForm()
    data = [{'id': 0, 'class_name': '---------'},]
    classes = data + classes
    choices = [(option['id'], option['class_name']) for option in classes]
    form = PaperDetailForm(choices=choices)
    
    context = {'form':form}
    return render(request,'ToolCore/paper-detail-form.html',context)

def bookChapter(request):
    subject_id = request.session.get('subject_id')
    book_response = requests.get('http://54.252.241.208/api/v1/subjects/' + str(subject_id) + '/books/')
    books = book_response.json()
    form = {
        'school_name':request.session.get('school_name'),
        'class_name':request.session.get('class_name'),
        'subject_name':request.session.get('subject_name'),
        'exam_name':request.session.get('exam_name'),
        'date':request.session.get('date'),
        'duration':request.session.get('duration'),
        'marks':request.session.get('marks'),
        'rows':request.session.get('rows'),
    }



    BookChapter = {}
    for book in books:
        chapter_response = requests.get('http://54.252.241.208/api/v1/books/' + str(book['id']) + '/chapters/')
        chapters = chapter_response.json()
        BookChapter[book['book_name']]=chapters
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        selected_chapters = []
        for id in selected_ids:
            chapter_detial = requests.get('http://54.252.241.208/api/v1/chapters/' + str(id) + '/')
            chapterDetail = chapter_detial.json()
            selected_chapters.append(chapterDetail)
        
        context = {'form':form,'BookChapter':BookChapter,'chapters':selected_chapters}

        return render(request,'ToolCore/toolpage.html',context)
    
    context = {'form':form,'BookChapter':BookChapter}
    return render(request,'ToolCore/book-chapter.html',context)


def viewPDF(request):
    
    if request.method == 'POST':
        question_ids = request.POST.getlist('questionIds[]')
        question_list = json.loads(request.POST.get('questionList', '[]'))
        allquestion = json.loads(request.POST.get('allquestion', '[]'))
        papersection = json.loads(request.POST.get('papersection'))
        questions = []
        # data = {'question_ids':question_ids,'question_list':question_list}
        # print(question_ids)
        # for id in question_ids:
        #     question_response = requests.get('http://127.0.0.1:8000/api/v1/' + id + '/')
        #     question = question_response.json()
        #     question['marks']= next((item['marks'] for item in marks if item['questionId'] == id), None)
        #     question['serialno']= next((item['serialno'] for item in marks if item['questionId'] == id), None)
        #     questions.append(question)

        # print(allquestion)
        for item in allquestion:
            
            if item['id1'][0]!='q':
                question_response = requests.get('http://54.252.241.208/api/v1/' + item['id1'] + '/')
                question = question_response.json()
                if item['id1'][0]=='m':
                    item['answer1']=question['correct_option']
                else:
                    item['answer1']=question['answer']
            
            if item['id2']!=None and item['id2'][0]!='q':
                question_response = requests.get('http://54.252.241.208/api/v1/' + item['id2'] + '/')
                question = question_response.json()
                if item['id2'][0]=='m':
                    item['answer2']=question['correct_option']
                else:
                    item['answer2']=question['answer']
        print(allquestion)

        request.session['questions'] = questions
        request.session['customquestions'] = question_list
        request.session['allquestion'] = allquestion
        request.session['papersection']= papersection
        
        

        return JsonResponse({'message': 'Data received and processed successfully'})

    # Return an error response if the request method is not POST or it's not an AJAX request
    return JsonResponse({'error': 'Invalid request'})


def paper(request):
    papersection = request.session.get('papersection')
    
# 'data':data,'form':form,'questions':questions,'customquestions':customquestions,
    
    return render(request,'ToolCore/paper.html',{'papersection':papersection})

def paperSolution(request):
    # data = request.GET.get('data')
    form = {
        'school_name':request.session.get('school_name'),
        'class_name':request.session.get('class_name'),
        'subject_name':request.session.get('subject_name'),
        'duration':request.session.get('duration'),
        'marks':request.session.get('marks'),
        'exam_name':request.session.get('exam_name'),
    }
    
    questions = request.session.get('questions')
    customquestions = request.session.get('customquestions')
    allquestion = request.session.get('allquestion')
    context = {'questions':questions,'customquestions':customquestions,'allquestion':allquestion,'form':form}
    return render(request,'ToolCore/paperSolution.html',context)


def profile(request):
    return render(request,'ToolCore/profile.html')