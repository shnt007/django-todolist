from re import template
from django.contrib import admin

from django.shortcuts import render
from django.http import HttpResponse
from datetime import date
import calendar
from calendar import HTMLCalendar

#importing forms
from todolist.form import UserTaskForm
from todolist.form import AssignedTaskDescForm
from todolist.form import UserNoteForm
from todolist.form import PersonalTaskForm

#importing models
from todolist.form import UserNote

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

'''def note_delete(request, note_id):
    user_delete = UserNote.object.get(id = note_id)
    return render(request, 'note/delete.html',{'data':user_delete})'''

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