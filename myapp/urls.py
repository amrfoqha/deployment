from django.urls import path
from . import views



urlpatterns=[
    path('', views.root),
    path('register', views.register),
    path('login', views.login),
    path('view_welcome', views.view_welcome),
    path('logout', views.logout),
    path('view_create_project', views.view_create_project),
    path('create_project', views.create_project),
    path('view_project/<int:id>', views.view_project),
    path('join_project/<int:id>', views.join_project),
    path('leave_project/<int:id>', views.leave_project),
    path('delete_project/<int:id>', views.delete_project),
    path('view_edit_project/<int:id>', views.view_edit_project),
    path('edit_project', views.edit_project),
    
]