from django import forms
from django.contrib.auth.models import User
from django.core import validators
from login_app.models import UserProfileInfo
class SearchFriend(forms.Form):
    friend_name = forms.CharField()

class BasicInfoForm(forms.ModelForm):
    #we have a password attribute that we want to edit a bit
    #thats why we had it like that


    class Meta():
        model = User
        fields = ('username', 'email')
###########Password Matcher Validator######################
    def clean_email(self):
        cleaned_data = super(BasicInfoForm, self).clean()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required")
        return email #By convention

class UpdatePasswordForm(forms.ModelForm):
    #we have a password attribute that we want to edit a bit
    #thats why we had it like that
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('password',)
###########Password Matcher Validator######################

    def clean_password_again(self):
        cleaned_data = super(UpdatePasswordForm, self).clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')
        if password != password_again:
            raise forms.ValidationError("Passwords do not match")
        return password_again #By convention


     #botcatcher = forms.CharField(required=False, widget = forms.HiddenInput,
    #                               validators=[validators.MaxLengthValidator(0)])




class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_picture',)
