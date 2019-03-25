from django import forms
from login_app.models import UserProfileInfo
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    #we have a password attribute that we want to edit a bit
    #thats why we had it like that
    password = forms.CharField(widget=forms.PasswordInput())
    password_again = forms.CharField(widget=forms.PasswordInput())

    class Meta():
        model = User
        fields = ('username', 'email', 'password')
###########Password Matcher Validator######################
    def clean_password_again(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        password_again = cleaned_data.get('password_again')
        if password != password_again:
            raise forms.ValidationError("Passwords do not match")
        return password_again #By convention

    def clean_email(self):
        cleaned_data = super(UserForm, self).clean()
        email = cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("This field is required")
        return email #By convention

class UserProfileInfoForm(forms.ModelForm):
    class Meta():
        model = UserProfileInfo
        fields = ('profile_picture',)

#Notice: they all belong to the same model class although they represent two different forms
