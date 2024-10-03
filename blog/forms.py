# accounts/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile,CreatePost
from PIL import Image
# from ckeditor.widgets import CKEditorWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_pic=forms.ImageField(required=False)
    
    class Meta:
        model = User
        fields = ('first_name','last_name','username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists")
        return email
    
    def clean_profile_pic(self):
        try:
            image=Image.open(self.file)
            image.verify()
            return True
        except:
            raise  forms.ValidationError("pl choose image file")






class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password=forms.CharField(widget=forms.PasswordInput)
    
class updateProfile(forms.ModelForm):
    class Meta:
        model=UserProfile
        fields=['profile_pic']


class Create_Post(forms.ModelForm):
  
    class Meta:
        model=CreatePost
        fields=['title','content']


class UserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=["username","first_name","last_name"]