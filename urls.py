"""KTUstudymates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from myapp import views

urlpatterns = [
    path('login/', views.login),
    path('loginpost/',views.login_post),
    path('home/',views.home),
    path('mentorreg/',views.mentorreg),
    path('mentorreg_post/',views.mentorreg_post),
    path('mentoredit/<id>',views.mentoredit),
    path('mentoredit_post/',views.mentoredit_post),
    path('mentorview/', views.mentorview),
    path('mentordelete/<id>', views.mentordelete),
    path('search_post/', views.search_post),
    path('feedbakview/', views.feedbackview),
    path('feedbackview_post/', views.feedbackview_post),
    path('changepasswd/', views.changepasswd),
    path('changepasswd_post/', views.changepasswd_post),
    path('complaintreply/<id>', views.complaintreply),
    path('complaintreply_post/', views.complaintreply_post),
    path('complaintview/', views.complaintview),
    path('complaintview_post/', views.complaintview_post),
    path('studentview/', views.studentview),
    path('searchstud_post/', views.searchstud_post),
    path('viewreview/', views.viewreview),
    path('viewreview_post/', views.viewreview_post),
    path('logout/', views.logout),
    ##########################
    path('home_mentor/', views.home_mentor),
    path('Viewprofile/', views.Viewprofile),
    path('Subjectview/', views.Subjectview),
    path('Viewpqp/', views.Viewpqp),
    path('Viewnotes/', views.Viewnotes),
    path('Editsubject/<id>', views.Editsubject),
    path('EditSubjectpost/', views.EditSubjectpost),
    path('Editpqp/<id>', views.Editpqp),
    path('Editpqp_post/', views.Editpqp_post),
    path('Editnotes/<id>', views.Editnotes),
    path('Editnotes_post/', views.Editnotes_post),
    path('Addsubject/', views.Addsubject),
    path('Addsubject_post/', views.Addsubject_post),
    path('Addpqp/', views.Addpqp),
    path('Addpqp_post/', views.Addpqp_post),
    path('Addnotes_post/', views.Addnotes_post),
    path('Addnotes/', views.Addnotes),
    path('subjectdelete/<id>', views.subjectdelete),
    path('pqpdelete/<id>', views.pqpdelete),
    path('notesdelete/<id>', views.notesdelete),
    path('doubtview/', views.doubtview),###
    path('doubtview_post/', views.doubtview_post),###
    path('doubtreply/<id>', views.doubtreply),###
    path('doubtreply_post/', views.doubtreply_post),###

    path('viewstudent/',views.viewstudent),
    path('viewstudent_post/',views.viewstudent_post),


    #####################################
    path('studentlogin/', views.studentlogin),
    path('studentsignup/', views.studentsignup),
    path('studentchangepassword/', views.studentchangepassword),
    path('studentviewprofile/', views.studentviewprofile),
    path('studenteditprofile/', views.studenteditprofile),
    path('studentviewtutor/', views.studentviewtutor),
    path('studentviewsubject/', views.studentviewsubject),
    path('studentviewpqp/', views.studentviewpqp),
    path('studentchattutor/', views.studentchattutor),
    path('studentviewnotes/', views.studentviewnotes),
    path('studentchattutor/', views.studentchattutor),
    path('studentsendcomplaint/', views.studentsendcomplaint),
    path('studentviewcomplaintreply/', views.studentviewcomplaintreply),
    path('studentfeedback/', views.studentfeedback),
    path('studentmentorreview/', views.studentmentorreview),
    path('studentmentorGD/', views.studentmentorGD),
    path('studentsubjectdoubts/', views.studentsubjectdoubts),
    path('studentviewdoubtsreply/', views.studentviewdoubtsreply),
    # path('chat1/<id>', views.chat1),
    # path('chat_view1/', views.chat_view1),
    # path('chat_send1/', views.chat_send1),
    path('studentsendreview/', views.studentsendreview),
    path('User_sendchat/',views.User_sendchat),
    path('User_viewchat/', views.User_viewchat),
    path('chat1/<id>', views.chat1),
    path('chat_view/', views.chat_view),
    path('chat_send/<msg>', views.chat_send),
    path('User_viewGroupchat/', views.User_viewGroupchat),
    path('User_sendGroupchat/', views.User_sendGroupchat),
    path('chat/', views.chat),



]

