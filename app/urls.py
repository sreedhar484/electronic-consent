from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.home,name='home'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    # path('acconts/',include('django.contrib.auth.urls')),
    # path('acconts/logout',include('django.contrib.auth.urls')),
    path('signup',views.register,name='signup'),
    path('log',views.log,name='log'),
    path('profile',views.profile,name="profile"),
    path('createdoc',views.createdoc,name='createdoc'),
    path('alldoc',views.alldoc,name='alldoc'),
    path('allparticipents',views.allparticipents,name='allparticipents'),
    path('pendingdoc',views.pendingdoc,name='pendingdoc'),
    path('signeddoc',views.signeddoc,name='signeddoc'),
    path('declineddoc',views.declineddoc,name='declineddoc'),
    path('draftdoc',views.draftdoc,name='draftdoc'),
    path('sign/<id>',views.sign,name='sign'),
    path('decline/<id>',views.decline,name='decline'),
    path('draft/<id>',views.draft,name='draft'),
    path('revoke/<id>',views.revoke,name='revoke'),
    path('viewdetails/<id>',views.viewdetails,name='viewdetails'),
    path('feedback',views.feedback,name='feedback'),
    path('viewparticipent/<id>',views.viewparticipent,name='viewparticipent'),
    path('editdoc/<id>',views.editdoc,name='editdoc'),
    
]