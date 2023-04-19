from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from social.models import UserProfile,Posts


class RegistationForm(UserCreationForm):

    class Meta:
        model=User
        fields=["username","password1","password2"]

        widgets={
        "username" : forms.TextInput(attrs={"class":"form-control" }),
        "password1" : forms.TextInput(attrs={"class":"form-control" }),
        "password2" : forms.PasswordInput(attrs={"class":"form-control" }),
  
    }
    
class LoginForm(forms.Form):
    username=forms.CharField(widget=forms.TextInput(attrs={"class":"form-control"}))
    password=forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control"}))


class UserProfileForm(forms.ModelForm):
    class Meta:
        model=UserProfile
        exclude=("user",)

        widgets={
        "bio" : forms.TextInput(attrs={"class":"form-control" }),
        "profile_pic":forms.FileInput(attrs={"class":"form-control"}),
        "cover_pic":forms.FileInput(attrs={"class":"form-control"}),
        "dob" : forms.DateInput(attrs={"class":"form-control" ,"type":"date"}),
        "phone" : forms.TextInput(attrs={"class":"form-control" }),
  
    }
        
class PostForm(forms.ModelForm):
    class Meta:
        model=Posts
        fields=["title","image"] 
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "image":forms.FileInput(attrs={"class":"form-control"})
        }