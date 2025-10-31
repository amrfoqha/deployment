import datetime
import datetime
import re
from django.db import models
from django.contrib import messages
import bcrypt


class UserMangaer(models.Manager):
    def register_validation(self,postdata):
        errors={}
        if len(postdata.get('first_name',''))<2:
            errors['first_name']="name must be at least 2 characters"
        if len(postdata.get('last_name',''))<2:
            errors['last_name']="name must be at least 2 characters"
        if len(postdata.get('email',''))<=0:
            errors['email']="fil all the input field"
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', postdata.get('email','')):
            errors['email1']="Email should be Valid"
        elif is_exists(postdata.get('email','')):
            errors['email2']="email already exists"
        if len(postdata.get('password',''))==0:
            errors['password']="fil all the input field"
        if len(postdata.get('password',''))<8:
            errors['password']="password should be at least 8 characters"    
        if len(postdata.get('con_password',''))<=0:
            errors['con_password']="fil all the input field"
        if postdata.get('password','')!=postdata.get('con_password','')  :
            errors['confirm_password']="Passwords should be match"
        return errors    
    
    def login_validation(self,postdata):
        errors={}
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', postdata.get('email','')):
            errors['email']="Email should be Valid"
        elif not is_exists(postdata['email']):    
            errors['login']="Email provided not found"    
        if len(postdata['password'])<=0 :
            errors['password']="Please Enter Password"
        return errors       

    def project_validation(self,postdata):
        errors={}
        if len(postdata.get('name',''))<2:
            errors['name']="name should be Valid and 2 characters"  
        if len(postdata['description'])<=0 :
            errors['description']="description is required"  
        if len(postdata.get('description',''))<=0:
            errors['description']="fil all the input field"
        if len(postdata.get('start_date',''))==0:
            errors['start_date']="fil all the input field" 
        else:    
            start_date_str=postdata.get('start_date')  
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()    
            if start_date  < datetime.date.today():
                errors['start_date'] = "start date can't be in the past" 
        if len(postdata.get('end_date','')) == 0:
            errors['end_date']="fil all the input field"
        else:    
            end_date_str=postdata.get('end_date')  
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()     
            if end_date  < datetime.date.today() or end_date < start_date :
                errors['End'] = "End date must be in present and after start date" 
        return errors 
        
        
class User(models.Model):
    first_name=models.CharField(max_length=25);
    last_name=models.CharField(max_length=25);
    email=models.CharField(max_length=100);
    password=models.CharField();
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserMangaer()
    
class Project(models.Model):
    name=models.CharField(max_length=25)
    description=models.TextField(max_length=350)
    start_date=models.DateTimeField()
    end_date=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=UserMangaer()
    user=models.ForeignKey(User,related_name='projects',default=None,on_delete=models.CASCADE,null=True)
    
class batata(models.Model):
    user=models.ForeignKey(User,related_name='users',on_delete=models.CASCADE,default=None,null=True)   
    project=models.ForeignKey(Project,related_name='in_projects',on_delete=models.CASCADE,default=None,null=True)
         
            

def is_exists(email):
    return User.objects.filter(email=email).exists()    
def search_user(email):
    return User.objects.filter(email=email)[0]    
def create_user(request):
    errors=User.objects.register_validation(request.POST);
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,f"reg_{key}")
        return False
    
    password = request.POST['password']
    hash1=bcrypt.hashpw(password.encode(),bcrypt.gensalt()).decode()   
    first_name=request.POST['first_name'] 
    last_name=request.POST['last_name'] 
    email=request.POST['email'] 
    user=User.objects.create(first_name=first_name,last_name=last_name,email=email,password=hash1)
    request.session['user_id']=user.id
    request.session['logged_in']=True
    return True
            
def login_user(request):
    errors=User.objects.login_validation(request.POST);
    if len(errors)>0:
        for key,val in errors.items():
            messages.error(request,val,f"log_{key}")
        return False
    email=request.POST['email'] 
    user=search_user(email)
    password = request.POST['password']
    if bcrypt.checkpw(password.encode(),user.password.encode()):
        request.session['user_id']=user.id
        request.session['logged_in']=True
        return True
    else:
        messages.error(request,'Wrong password or email','log_password')
        return False
    
def get_user(id):
    return User.objects.get(id=id)    
           
    
def new_project(request):
    errors=User.objects.project_validation(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request,value,f'project_{key}')
        return False
    name=request.POST['name']    
    description=request.POST['description']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    
    user=get_user(request.session['user_id'])
    project=Project.objects.create(name=name,start_date=start_date,end_date=end_date,description=description,user=user)
    return True
def get_all_projects():
    return Project.objects.all()  

def get_project(id):
    return Project.objects.get(id=id)
def link_user_project(user_id,project_id):
    btbt=batata.objects.create(user=get_user(user_id),Project=get_project(project_id))
def is_member(user_id,project_id):
    return batata.objects.filter(user=user_id,project=project_id).exists()

def get_btbt(user_id):
    # user=get_user(user_id)
    # result=batata.objects.filter(user=user)
    return  Project.objects.filter(in_projects__user_id=user_id)


def join_user_to_project(user_id,project_id):
    user=get_user(user_id)
    project=get_project(project_id)
    batata.objects.create(user=user,project=project)
def leave_user_to_project(user_id,project_id):
    user=get_user(user_id)
    project=get_project(project_id)
    btbt=batata.objects.filter(user=user,project=project)
    btbt.delete()
    
def get_project_team(id):
     return User.objects.filter(users__project_id=id)
 
def remove_project(id):
    proj=Project.objects.get(id=id)
    proj.delete()
    
def update_project(id,request):
    errors=User.objects.project_validation(request.POST)
    if errors:
        for key,value in errors.items():
            messages.error(request,value,f'project_{key}')
        return False
    name=request.POST['name']    
    description=request.POST['description']
    start_date=request.POST['start_date']
    end_date=request.POST['end_date']
    id=request.POST['hidden']
    
    project=Project.objects.get(id=id)
    project.name=name
    project.description=description
    project.start_date=start_date
    project.end_date=end_date
    project.save()
    return True
         