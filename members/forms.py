from django import forms
from .models import Profile

class Profilephoto(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo' ,)