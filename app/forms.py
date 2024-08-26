from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . models import Profile,ConsentDocument

class ExtendedForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username','email','first_name','last_name','password1','password2')

class ProfileForm(forms.ModelForm):
    photo = forms.ImageField(required=False)
    class Meta:
        model = Profile
        fields = ('photo','bio','acc_type')

class ExtendedUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo','bio')

class ConsentDocumentForm(forms.ModelForm):
    class Meta:
        model=ConsentDocument
        fields = ('title','description','content')