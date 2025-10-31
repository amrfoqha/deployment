from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def root(request):
    if 'user_id' not in request.session:
        request.session['user_id']=None
    if 'logged_in' not in request.session:
        request.session['logged_in']=False
    return render(request,"home.html")

def register(request):
        if create_user(request):
            return redirect('/view_welcome')
        return redirect('/')

def login(request):
        if login_user(request):
            return redirect('/view_welcome')
        return redirect('/')

def view_welcome(request):
    if request.session['logged_in']== True:
        btbts=get_btbt(request.session['user_id'])
        joined_project_ids = btbts.values_list('id', flat=True)
        context={
            'user':get_user(request.session['user_id']),
            'projects':get_all_projects(),
            'joined_project_ids': joined_project_ids
        }
        return render(request,'welcome.html',context)
    return redirect('/')    
def logout(request):
    del  request.session['user_id']
    del  request.session['logged_in']
    return redirect('/')
def view_create_project(request):
    if 'logged_in' in request.session:
        context={
            'user':get_user(request.session['user_id']),
        }
        return render(request,'view_create_project.html',context)
    return redirect('/')
def create_project(request):
    if request.session['logged_in']== True: 
        if new_project(request):
            return redirect('/view_welcome')
        return redirect('/view_create_project')
    return redirect('/')


def view_project(request,id):
    context={
        'project':get_project(id),
        'user':get_user(request.session['user_id']),
        'teammates':get_project_team(id)
    }
    return render(request,'project.html',context)

def join_project(request,id):
    join_user_to_project(request.session['user_id'],id)
    return redirect('/view_welcome')

def leave_project(request,id):
    leave_user_to_project(request.session['user_id'],id)
    return redirect('/view_welcome')

def delete_project(request,id):
    remove_project(id)
    return redirect(f'/view_welcome') 



def view_edit_project(request,id):
    context={
        'user':get_user(request.session['user_id']),
        'project':get_project(id)
    }
    return render(request,'edit_project.html',context)


def edit_project(request):
    if update_project(id,request):
        return redirect(f'/view_welcome') 
    else:
        return redirect(f'/view_project/{id}') 
