"""boxydots_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from login_app import views as login_app
from profile_app import views as profile_app


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/',login_app.login,name='login'),
    path('logout/',login_app.user_logout,name='logout'),
    path('register/',login_app.register,name='register'),
    #path('/friends-list/<int:pk>/', profile_app.update_friend, name='update_friend'),
    path('friends-list/update/<int:id>/', profile_app.update_friend, name='update_friend'),
    path('profile/update_pw/', profile_app.update_pw, name='update_pw'),
    path('profile/update_info/', profile_app.update_info, name='update_info'),
    path('profile/update_pic/', profile_app.update_pic, name='update_pic'),

    path('',profile_app.lastGames, name='index'),

    path('last-games/',profile_app.lastGames, name='lastGames'),
    path('friends-list/',profile_app.friendsList, name='friendsList'),
    path('profile/',profile_app.profile, name='profile'),
    path('simulator/',profile_app.simulator, name='simulator'),
]
