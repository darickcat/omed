"""
Definition of views.
"""

from datetime import datetime
from django.http import HttpRequest, HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages  
import itertools
from django.db import models
from .models import Blog
from.models import Comment # использование модели комментариев
from.forms import CommentForm, BlogForm # использование формы ввода комментария
from django.http import HttpResponseNotAllowed

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        })

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
def register(request):  
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            form.save()  
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],)
            login(request, new_user)
            return redirect('home')  
        else:
            errors = form.errors.values()
            context = {  
                'form':form,
                'messages':list(itertools.chain(*errors))
            }  
            return render(request, 'app/registration.html', context) 
  
    else:  
        form = UserCreationForm()  
        context = {  
            'form':form  
        }  
        return render(request, 'app/registration.html', context)  

def blog(request):
 """Renders the blog page."""
 posts = Blog.objects.order_by('-posted') # запрос на выбор всех статей из модели, отсортированных по убыванию даты
                                          # опубликования
 assert isinstance(request, HttpRequest)
 return render(request,
     'app/blog.html',
     { # параметр в {} — данные для использования в шаблоне.
     'title':'Блог',
     'posts': posts, # передача списка статей в шаблон веб-страницы
     'year':datetime.now().year,
     })

def blogpost(request, parametr):
 """Renders the blogpost page."""
 post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
 assert isinstance(request, HttpRequest)
 comments = Comment.objects.filter(post=parametr)
 if request.method == "POST": # после отправки данных формы на сервер методом POST
     form = CommentForm(request.POST)
     if form.is_valid():
         comment_f = form.save(commit=False)
         comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
         comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
         comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
         comment_f.save() # сохраняем изменения после добавления полей

         return redirect('blogpost', parametr=post_1.id) # переадресация на ту же  страницу статьи после отправки комментария
 else:
         form = CommentForm() 
 return render(request,
         'app/blogpost.html',
         {
         'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы
         'year':datetime.now().year,
         'comments': comments, # передача всех комментариев к данной статье в шаблон  веб-страницы
         'form': form, 
         })

def newpost(request):
 if not request.user.is_superuser:
     return HttpResponseNotAllowed ("")
 if request.method == "POST": 
     form = BlogForm(request.POST, request.FILES)
     if form.is_valid():
         blog_f = form.save(commit=False)
         blog_f.posted = datetime.now()
         blog_f.save()

         return redirect('blogpost', parametr=blog_f.id)
     else:
         print (form.errors)
 else:
     form = BlogForm()
     return render(request,
         'app/newpost.html',
         {
         'form': form, 
         })

def links (request):
    return render(request,
         'app/links.html')