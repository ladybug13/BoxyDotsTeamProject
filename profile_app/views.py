from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from profile_app.models import FriendList
from profile_app.forms import UserProfileInfoForm, BasicInfoForm, UpdatePasswordForm, SearchFriend
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.
@login_required
def friendsList(request):

    username = request.user.username
    user = request.user
    searchResult=""
    # friend1 = request.friend_list.user1
    #friend2 = request.friendlist.user2
    #friendcol1 = FriendList.objects.filter(user1__username=username)
    #friendcol2 = FriendList.objects.filter(user2__username=username)
    # Because we are putting the method it will return the same thing as above!
    friendsConfirmed = FriendList.objects.raw(
       "SELECT * FROM profile_app_friendlist WHERE( user1_id={user1_id} OR user2_id={user1_id} )AND confirmed=1".format(user1_id=user.id)
       #saerch by username it is made by django but by raw sqlite it will be made by searcjing ids
    )
    friendsUnconfirmed = FriendList.objects.raw(
       "SELECT * FROM profile_app_friendlist WHERE( user1_id={user1_id} OR user2_id={user1_id} )AND confirmed=0".format(user1_id=user.id)
       #saerch by username it is made by django but by raw sqlite it will be made by searcjing ids
    )
    #*=select all columns !! NOT ROWS
    #friends = FriendList.objects.get(user1 = user, )
    #friend2 = FriendList.objects.get(user2 = user,

    if request.method == "POST":
        print('method is post')
        search_friend_form = SearchFriend(data = request.POST)
        notFriendYet=True
        if search_friend_form.is_valid():
            friendBeingSearched = search_friend_form.cleaned_data['friend_name']
            print(friendBeingSearched)
            friend = User.objects.raw(
               "SELECT id,username FROM auth_user WHERE username='{friendBeingSearched}'".format(friendBeingSearched=friendBeingSearched)
               #saerch by username it is made by django but by raw sqlite it will be made by searcjing ids
            )[:]
            print(friend)

            try :
                if user==friend[0]:
                    raise Exception("U can't add you as a friend")
                else:
                    allFriendships = FriendList.objects.raw(
                       "SELECT * FROM profile_app_friendlist WHERE( user1_id={user1_id} OR user2_id={user1_id} )".format(user1_id=user.id)
                       #saerch by username it is made by django but by raw sqlite it will be made by searcjing ids
                    )[:]
                    for frienship in allFriendships:
                        if FriendList(user1=user, user2=friend[0])==friendship:
                          raise Exception("That friendship was already attempted")
                          notFriendYet=False

                if notFriendYet:
                    newfriend = FriendList(user1=user, user2=friend[0])
                    newfriend.save()
                    searchResult="Your Friend Request Was Sent"
            except :
                searchResult="No results! Remeber you can't add yourself nor friends that you already have or that are currently on your confirming list"

        else: #if one or both of the forms dont work
            print(user_form.errors, profile_form.errors)
            error = True
    else:
        search_friend_form = SearchFriend()
        print('method is not post')

    return render(request,'profile_app/friends_list.html',{'username':username, 'friendsConfirmed':friendsConfirmed, 'friendsUnconfirmed':friendsUnconfirmed, 'searchResult':searchResult, 'searchEngine':search_friend_form})

@login_required
def lastGames(request):
    username = request.user.username
    return render(request,'profile_app/last_games.html',{'username':username})

@login_required
def profile(request):

    user = request.user
    username = request.user.username
    basic_info_form = BasicInfoForm()
    update_password_form = UpdatePasswordForm()
    profile_form = UserProfileInfoForm()
    print('method is not post')

    return render(request,'profile_app/profile.html',{'username':username, 'basic_info_form':basic_info_form, 'user':user, 'update_password_form':update_password_form, 'profile_form':profile_form })

@login_required
def simulator(request):
    username = request.user.username
    return render(request,'profile_app/simulator.html',{'username':username})

@login_required
def update_friend(request, id):
    user = request.user
    username = request.user.username
    friendsToBeConfirmed = FriendList.objects.raw(
       "SELECT * FROM profile_app_friendlist WHERE(( user1_id={user1_id} OR user2_id={id} )AND confirmed=0)OR(( user1_id={id} OR user2_id={user1_id} )AND confirmed=0)".format(user1_id=user.id, id=id)
       #saerch by username it is made by django but by raw sqlite it will be made by searcjing ids
    )[:]


    try :
        friendToBeConfirmed = friendsToBeConfirmed[0]
        friendToBeConfirmed.confirmed =1
        friendToBeConfirmed.save()

        if (friendToBeConfirmed.user1 == user):
            messages.success(request, 'You and {friend} are now friends!'.format(friend = friendToBeConfirmed.user2))
        else:
            messages.success(request, 'You and {friend} are now friends!'.format(friend = friendToBeConfirmed.user1))
    except :
        msg='Something Unexpected happen'
        messages.success(request, 'Something Wrong Happened')
        #friendToBeConfirmed = 0

    return redirect("/friends-list/")

@login_required
def update_info(request):
    user = request.user
    username = request.user.username

    basic_info_form = BasicInfoForm(data = request.POST)

    user_username = request.POST.get('username')
    email = request.POST.get('email')

    if basic_info_form.is_valid():
        basic_info_form_username = basic_info_form.cleaned_data['username']
        basic_info_form_email = basic_info_form.cleaned_data['email']
        user.username = basic_info_form_username
        user.email = basic_info_form_email
        user.save()
        #messages.success(request, 'You just got your email or username updated')
        print('basic info updated')
    elif username == user_username:
        basic_info_form_email = basic_info_form.cleaned_data['email']
        user.email = basic_info_form_email
        user.save()
        #messages.success(request, 'You just got your email or username updated')
        print('basic info updated')
    else: #if one or both of the forms dont work

        print(basic_info_form.errors)
        messages.error(request, basic_info_form.errors)


    return redirect("/profile/")

    #return render(request,'profile_app/friends_update.html',{'username':username, 'friendToBeConfirmed':friendToBeConfirmed, 'msg':msg})

@login_required
def update_pw(request):
    user = request.user
    username = request.user.username

    update_password_form = UpdatePasswordForm(data = request.POST)

    if update_password_form.is_valid():
        user.set_password(user.password) #This is hashing the password
        user.save()
        #messages.success(request, 'You just got your password updated')
        print('password updated')
    else: #if one or both of the forms dont work
        print(update_password_form.errors)
        error2 = True

    return redirect("/profile/")


@login_required
def update_pic(request):
    user = request.user
    username = request.user.username
    profile_form = UserProfileInfoForm(data = request.POST)

    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.user = user
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture'] # a dictionary of all the files they uploaded in the reuqets
            #its similar with other types of FILES
            #U'll be dealing with the key that you defined in your modes file
            profile.save()
            print('profile updated ')
            #messages.success(request, 'You just got your profile picture updated')
    else: #if one or both of the forms dont work
        print(profile_form.errors)
        messages.success(request, 'opps, Something wrong happened')

    return redirect("/profile/")
