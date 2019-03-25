from django.shortcuts import render
#We only import the forms, not the models in order to send them
from login_app.forms import UserProfileInfoForm, UserForm
#For logins imports:
from django.urls import reverse
#if you ever need a view that requires the user to be logged in, u can use this decoraor
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as log_in
from django.contrib import messages


# Create your views here.
def login(request):
        error_message = ""
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username = username,  password=password)

            if user:
                if user.is_active:
                    log_in(request, user)
                    return HttpResponseRedirect(reverse('index'))

                else:
                    error_message = "Account is not active"

            else:
                error_message = "Invalid login details supplied!"
        return render(request,'login_app/login.html', {'errormessage':error_message})

def register(request):
        print('This is register page')
        if request.method == "POST":
            #username = request.POST.get('username')
            #email = request.POST.get('email')


            user_form = UserForm(data = request.POST)
            profile_form = UserProfileInfoForm(data = request.POST)

            if user_form.is_valid() and profile_form.is_valid():
            #we gonna do different actions if they are profile details or user details

                user = user_form.save() #it pics the data collected from user_form and saves directly to the database
                user.set_password(user.password) #This is hashing the password
                user.save()
                #so: we grab the user form, the save it to the database then hashing the password, then
                print('user is saved')
                profile = profile_form.save(commit=False)

                profile.user = user
                print('profile gort associated with user')


                if 'profile_picture' in request.FILES:
                    profile.profile_picture = request.FILES['profile_picture'] # a dictionary of all the files they uploaded in the reuqets
                    #its similar with other types of FILES
                    #U'll be dealing with the key that you defined in your modes file
                    profile.save()

                    messages.success(request, 'You are registered!')

                log_in(request, user)
                return HttpResponseRedirect('/last-games')


                    #registered = True
            else: #if one or both of the forms dont work
                print(user_form.errors, profile_form.errors)
                #error = True
        else:
            user_form = UserForm()
            profile_form = UserProfileInfoForm()
            print('method is not post')

        return render(request,'login_app/register.html',{'user_form':user_form,'profile_form':profile_form , 'errormessage':"Something went Wrong"})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))
