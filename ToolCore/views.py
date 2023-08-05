from django.shortcuts import render,redirect
import requests
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponse
from .forms import PaperDetailForm
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.template import RequestContext
from django.views import View
from django.core.mail import send_mail
import json
import uuid
from .forms import UserLoginCreateForm,LoginForm
from .models import ToolLogin,UserLogin,Paper

def loginPage(request):
    page='login'
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not Exist')
        
        user = authenticate(request,email=email,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'User password is not Correct')
    context = {'page':page}
    return render(request,'ToolCore/login_register.html',context)

def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Error occured during registration')

    return render(request,'ToolCore/login_register.html',{'form':form})

def logoutUser(request):
    return redirect('home')



def toolPage(request):
    # chapter_response = requests.get('http://127.0.0.1:8000/api/v1/classes/8/subjects/9/chapters/')
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
    tool_user_id = request.session.get('tool_user_id')
    user = ToolLogin.objects.filter(tool_id=tool_user_id)
    context = {'form':form,'user_id':tool_user_id}
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

    tool_user_id = request.session.get('tool_user_id')
    user = ToolLogin.objects.get(tool_id=tool_user_id)
    papers = Paper.objects.filter(tool_login=user)
    remaining_papers=user.paper_credential-len(papers)


    BookChapter = {}
    for book in books:
        chapter_response = requests.get('http://54.252.241.208/api/v1/books/' + str(book['id']) + '/chapters/')
        chapters = chapter_response.json()
        BookChapter[book['book_name']]=chapters
    
    if request.method == 'POST':
        selected_ids = request.POST.getlist('selected_ids')
        request.session['selected_ids'] = selected_ids
        selected_chapters = []
        for id in selected_ids:
            chapter_detial = requests.get('http://54.252.241.208/api/v1/chapters/' + str(id) + '/')
            chapterDetail = chapter_detial.json()
            selected_chapters.append(chapterDetail)
           
        context = {'form':form,'BookChapter':BookChapter,'chapters':selected_chapters,'user':user,'papers':papers,'remaining_papers':remaining_papers}

        return render(request,'ToolCore/toolpage.html',context)
    
    context = {'form':form,'BookChapter':BookChapter,'user':user,}
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
        # print(allquestion)

        request.session['questions'] = questions
        request.session['customquestions'] = question_list
        request.session['allquestion'] = allquestion
        request.session['papersection']= papersection
        
        

        return JsonResponse({'message': 'Data received and processed successfully'})

    return JsonResponse({'error': 'Invalid request'})


def paper(request):
    papersection = request.session.get('papersection')

    school_name = request.session.get('school_name')
    exam_name = request.session.get('exam_name')
    class_name = request.session.get('class_name')
    subject_name = request.session.get('subject_name')
    tool_user_id = request.session.get('tool_user_id')
    tool_user = ToolLogin.objects.get(tool_id=tool_user_id)

    # Create and save the Paper object
    paper = Paper(
        tool_login=tool_user,
        school_name=school_name,
        exam_name=exam_name,
        class_name=class_name,
        subject_name=subject_name,
        paper_html=papersection
    )
    paper.save()
    return render(request,'ToolCore/paper.html',{'papersection':papersection,'paperId':paper.id})

from django.shortcuts import get_object_or_404

def save_paper(request, paper_id):
    paper = get_object_or_404(Paper, id=paper_id)

    if request.method == 'POST' and 'pdf_file' in request.FILES and 'pdf_file2' in request.FILES:
        pdf_file = request.FILES['pdf_file']
        pdf_file2 = request.FILES['pdf_file2']
        paper.saved_paper.save(pdf_file.name, pdf_file, save=True)
        paper.saved_solution.save(pdf_file2.name, pdf_file2, save=True)
        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'failure'})




def paperSolution(request):
    
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
    return render(request,'ToolCore/papersolution.html',context)


def profile(request):
    tool_user_id = request.session.get('tool_user_id')
    tool_user = ToolLogin.objects.get(tool_id=tool_user_id)
    papers = Paper.objects.filter(tool_login=tool_user)
    context = {
        'user':tool_user,
        'papers': papers,
    }
    return render(request,'ToolCore/profile.html',context)

def viewPaper(request,paper_id):
    tool_user_id = request.session.get('tool_user_id')
    user = ToolLogin.objects.get(tool_id=tool_user_id)
    papers = Paper.objects.filter(tool_login=user)
    remaining_papers=user.paper_credential-len(papers)
    paper = get_object_or_404(Paper, id=paper_id)

    context = {
        'user':user,
        'paper':paper,
    }
    return render(request,'Toolcore/paper.html',context)
def editPaper(request,paper_id):

    tool_user_id = request.session.get('tool_user_id')
    user = ToolLogin.objects.get(tool_id=tool_user_id)
    papers = Paper.objects.filter(tool_login=user)
    remaining_papers=10-len(papers)
    paper = get_object_or_404(Paper, id=paper_id)
    selected_chapters = []
    selected_ids = request.session.get('selected_ids')
    for id in selected_ids:
        chapter_detial = requests.get('http://54.252.241.208/api/v1/chapters/' + str(id) + '/')
        chapterDetail = chapter_detial.json()
        selected_chapters.append(chapterDetail)

    context = {
        'user':user,
        'paper':paper,
        'chapters':selected_chapters,
        'remaining_papers':remaining_papers
    }

    return render(request,'ToolCore/toolpage.html',context)

# login register


def verify(request,token):
    try:
        user_form = UserLogin.objects.get(email_token=token)
        user_form.is_verified = True
        tool_form = ToolLogin(
        user=user_form,
        name=user_form.name,
        email=user_form.email,
        tool_id=user_form.email,  
        tool_password=user_form.password,
        paper_credential=10,  
        )
        tool_form.save()
    except Exception as e:
        return HttpResponse(e)
    return redirect('home')

def UserRegister(request):
    if request.method == 'POST':
        form = UserLoginCreateForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            if password == confirm_password:
                user_form = form.save()
                user_form.email_token = str(uuid.uuid4())  
                user_form = form.save()
                subject='Welcome ' + user_form.name
                message='Thank you for registering.' + f'Click on the link to verify account http://54.252.241.208/verify/{user_form.email_token}/'
                send_mail(
                subject,
                message,
                'pintupatidar555@gmail.com',  
                [user_form.email], 
                fail_silently=False,
                )
                messages.success(request, 'Verify Account then login and simply use tool')
                # return render(request, 'ToolCore/homepage.html', {'user': user_form.name})
            else:
                messages.error(request, 'Passwords do not match.')
        else:
                email = request.POST.get('email')
                if UserLogin.objects.filter(email=email).exists():
                    messages.error(request, 'Please login you already have an account with these email.')
    else:
        form = UserLoginCreateForm()
    return render(request, 'ToolCore/UserLogin.html', {'form': form,'flag':'register'})

def User_Login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                user = UserLogin.objects.get(email=email)
                if user.password == password:
                    tool_user=ToolLogin.objects.filter(email=email)
                    request.session['tool_user_id']=email
                    return render(request, 'ToolCore/homepage.html', {'user': user.name}) 
                else:
                    # form.add_error('password', 'Invalid password')
                    messages.error(request, 'Invalid Password')
            except UserLogin.DoesNotExist:
                # form.add_error('email', 'User does not exist')
                messages.error(request, 'User does not exist')
    else:
        form = LoginForm()
    
    return render(request, 'ToolCore/UserLogin.html', {'form': form})


def home(request):
    if request.method == 'POST':
        tool_id = request.POST.get('toolId')
        tool_password = request.POST.get('toolPassword')
        if ToolLogin.objects.filter(tool_id=tool_id, tool_password=tool_password).exists():
            tool_user=ToolLogin.objects.filter(tool_id=tool_id)
            request.session['tool_user_id']=tool_id
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'failure'})
    return render(request,'ToolCore/homepage.html')




