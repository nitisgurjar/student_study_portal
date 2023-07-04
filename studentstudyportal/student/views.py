from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from . forms import *
from django.views import generic
from youtubesearchpython import VideosSearch
import requests

# Create your views here.
def books(request):
    return render(request,'books.html')
def home(request):
    return render(request,'home.html')
def notes(request):
    if request.method=='POST':
        form=NotesForm(request.POST)
        if form.is_valid:
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"notes added successfully")
    else:
      form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'notes.html',context)



def delete_note(request,pk):
    Notes.objects.get(id=pk).delete()
    return redirect('notes')

def delete_homework(request,pk):
    Homework.objects.get(id=pk).delete()
    return redirect('homework')




class NotesDetailView(generic.DetailView):
    model=Notes
def notesdetail(request,pk):
    note=Notes.objects.filter(id=pk)
    return render (request,'notes_detail.html',{'note':note})

def homework(request):
    if request.method=='POST':
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=='on':
                    finished= True
                else:
                    finished= False
            except:
                finished= False
            homeworks=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished

            )
            homeworks.save()
            messages.success(request,f"homework added successfully")
    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(user=request.user)
    if len(homework)== 0:
        homework_done= True
    else:
        homework_done= False

    return render(request,'homework.html',{'homework':homework,
                                           'homework_done':homework_done,
                                           'form':form})


def update_homework(request,pk):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished = False
    else:
        homework.is_finished = True
    homework.save()
    return redirect('homework')


def youtube(request):
    if request.method=='POST':
        form=SerachForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'view':i['viewCount']['short'],
                'published':i['publishedTime'],
            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc +=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
        return render(request,'youtube.html',{'form':form,'results':result_list})
    else:
       form=SerachForm()
    return render(request,'youtube.html',{'form':form})

def todo(request):
    if request.method=='POST':
        form=TodoForm(request.POST)
        if form.is_valid():
            try:
              finished=request.POST['is_finished']
              if finished == 'on':
                 finished = True
              else:
                finished = False
            except:
                finished= False
            todos=Todo(
                user=request.user,
                title=request.POST['title'],
                is_finished=finished
            )
            todos.save()
            messages.success(request,f"todos saved successfully")
    else:
      form=TodoForm()
    todo=Todo.objects.filter(user=request.user)
    if len(todo)==0:
        todo_done= True
    else:
        todo_done= False

    return render(request,'todo.html',{'todo':todo,'form':form,'todo_done':todo_done})



def update_todo(request,pk):
    todo=Todo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished = True
    todo.save()
    return redirect('todo')

def delete_todo(request,pk):
    Todo.objects.get(id=pk).delete()
    return redirect('todo')



def books(request):
    if request.method=='POST':
        form=SerachForm(request.POST)
        text=request.POST['text']
        url='https://www.googleapis.com/books/v1/volumes?q='+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                'description':answer['items'][i]['volumeInfo'].get('description'),
                'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                'categories':answer['items'][i]['volumeInfo'].get('categories'),
                'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                'preview':answer['items'][i]['volumeInfo'].get('previewLinks'),
                  }
           
            result_list.append(result_dict)
        return render(request,'books.html',{'form':form,'results':result_list})
    else:
       form=SerachForm()
    return render(request,'books.html',{'form':form})




