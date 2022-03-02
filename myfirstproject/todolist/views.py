from re import template
from django.contrib import admin

from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
import json
from calendar import HTMLCalendar
from django.core.mail import send_mail as sm

#importing forms
from todolist.form import UserLoginForm, UserProfileForm, UserTaskForm
from todolist.form import AssignedTaskDescForm
from todolist.form import UserNoteForm
from todolist.form import PersonalTaskForm
from todolist.form import UserRegistrationForm

# importing models
from todolist.models import UserNote, UserProfile
from todolist.models import User

# Create your views here.
def index(request, year=date.today().year, month=date.today().month):
    title = "This is a title"
    year = int(year)
    month = int(month)

    if year < 1999 or year > 2099:
        year = date.today().year
    
    month_name = calendar.month_name[month]

    cal = HTMLCalendar().formatmonth(year, month)

    title = "Current Month: " + month_name
    data = {'title':title, 'cal': cal , 'month': month}
    return render(request, "base.html", data)

def user_task(request):
    userTask = UserTaskForm
    return render(request, "index.html", {'form':userTask})

#loads the note index page
def note(request):
    note = UserNoteForm

    #method one by creating object and retrieving data
    un1 = UserNote
    un1.objects.all()

    #method two creating object and retrieving data at the time
    un2 = UserNote.objects.all()
    
    return render(request, 'note.html', {'form':note, "obj1":un1, "obj2":un2})

#stores the note data to database
def note_insert(request):
    template = 'note.html'

    #creating onject of form
    note = UserNoteForm

    #filtering request method
    if request.method == "POST":
        #filtering request data
        title = request.POST.get('note_title')
        desc = request.POST.get('note_description')
        add_at = request.POST.get('note_added_at')

        un = UserNote(note_title = title, note_description = desc, note_added_at = add_at)
        un.save()
        #success message
        msg = "Success"
        #sending response to request
        return render(request, template,{'form': note, 'msg': msg, 'data':un})
        #else:
         #   msg = 'Fail'
          #  return render(request, template,{'form': note, 'msg': msg})
    else:
        msg = "Something Went Wromg"
        return render(request, template,{'form': note, 'msg':msg})

#note - refractor
# note index -  this method display all list of notes    
def note_index(request):
    user_note = UserNote.objects.all()
    return render (request, 'notes/index.html',{'data':user_note})

#note create - this method loads form and stores data of note
def note_create(request):
    if request.method =="POST":
        title = request.POST.get('note_title')
        desc = request.POST.get('note_description')
        added_at = request.POST.get('note_added_at')

        un = UserNote(note_title = title, note_description = desc, note_added_at = added_at)
        un.save()
        msg = "Successfully stored"
        user_note = UserNote.objects.all()
        return render(request, 'notes/index.html',{ 'msg': msg, 'data':user_note})
    else:
        note = UserNoteForm
        msg = "Something Went Wromg"
        return render(request, 'notes/create.html',{'form': note, 'msg':msg})

def note_show(request, note_id):
    user_note = UserNote.objects.get(id = note_id)
    return render(request, 'notes/show.html', {'data':user_note})

def note_edit(request, note_id):
    user_edit = UserNote.objects.get(id = note_id)
    return render(request, 'notes/edit.html', {'data':user_edit})

def note_update(request):
    note_id = request.POST.get('id')
    if request.method =="POST":
        #data fetch by id
        note = UserNote.objects.get(id = note_id)
        note.note_title = request.POST.get('note_title')
        note.note_description = request.POST.get('note_description')
        note.note_added_at = request.POST.get('note_added_at')
        note.save()
        msg = "Successfully updated"
        user_note = UserNote.objects.all()
        return render(request,'notes/index.html',{'data':user_note, 'msg':msg})
    else:
        msg = "Something went wrong"
        user_edit = UserNote.objects.get(id = note_id)
        return render(request, 'notes/edit.html',{'data': user_edit, 'msg':msg})

def note_delete(request, note_id):
    #creating object by id and deleteing the object
    note = UserNote.objects.get(id = note_id)
    note.delete()

    #fetching remaning data and returning back to index page with data
    un = UserNote.objects.all()
    msg = "Delete successfully"
    return render(request, 'notes/index.html', {'data':un, 'msg':msg})

# send email
def send_email(request):
    # to take request from post method
    
    # res = sm(
    #     subject = request.POST.get('subject'),
    #     message = request.POST.get('message'),
    #     from_email = 'sushantd34@gmail.com'
    #     recipient_list = [request.POST.get('receiver_email')],
    #     fail_silently = False,
    # )

    res = sm(
        subject = 'Gmail Email Send Test',
        message = 'Here is the message we have send you to test our gmail send message',
        from_email = 'sushantd34@gmail.com',
        recipient_list = ['sd993037@gmail.com'],
        fail_silently = False,
        # fail_silently takes boolean value. If set False it will raise smtplib.STMPException if the error
        # occurs while sending the email
    )
    return HttpResponse(request, "Email send sucess" + str(res))

# user
def user_create(request):
    userForm = UserRegistrationForm 
    return render(request, 'users/create.html', {'form': userForm})

def user_index(request):
    if request.session.has_key('username'):
        username = request.session['username']
        return render(request, 'users/index.html', {'username': username})
    else:
        template = 'users/login.html'
        ul = UserLoginForm
        msg = "Please login to access"
        context = {'form':ul, 'msg': msg}
        return render(request, template, context)

def user_register(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        contact = request.POST.get('contact')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User(first_name=first_name, last_name=last_name, contact=contact, \
            username=username, password=password)
        user.save()

        # setting session
        request.session['username'] = username

        # checking session key if exist
        if request.session.has_key('username'):
            # getting session value
            uname = request.session['username']
            return render(request, 'users/index.html', {'username': uname})
    else:
        userForm = UserRegistrationForm 
        return render(request, 'users/create.html', {'form': userForm})

def user_login(request):
    template = 'users/login.html'
    form = UserLoginForm
    context = {'form':form}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if password == user.password:
            request.session['username'] = user.username
            if request.session.has_key('username'):
                uname = request.session['username']
                return render(request, 'users/index.html', {'username': uname})
        else:
            return render(request, template, context)
    else:
        return render(request, template, context)

def user_profile(request):
    if request.session.has_key('username'):
        username = request.session['username']
        user = User.objects.get(username=username)
        form = UserProfileForm
        if request.method == "POST":
            formSave = UserProfileForm(request.POST, request.FILES)
            if formSave.is_valid():
                formSave.save()
                return render(request, 'users/show.html', {'form': form, 'data': user})
        else:
            return render(request, 'users/show.html', {'form': form, 'data': user})
    else:
        formLogin = UserLoginForm
        return render(request, 'users/login.html', {'form': formLogin, 'msg': "please login to access"})

def user_logout(request):
    template = 'users/login.html'
    ul = UserLoginForm
    msg = "Please login to access"
    context = {'form':ul, 'msg': msg}
    if request.session.has_key('username'):
        del request.session['username']
        return render(request, template, context)
    else:
        return render(request, template, context)

'''def assigned_task_desc(request):
    assign = AssignedTaskDescForm
    return render(request, 'index.html', {'form':assign })

def personal_task(request):
    personal = PersonalTaskForm
    return render(request, 'index.html', {'form': personal})    

def user_note(request):
    note = UserNoteForm
    return render(request, 'index.html', {'form': note})

def custom(request):
    return HttpResponse("<html><body>This is custom page</body></html>")'''