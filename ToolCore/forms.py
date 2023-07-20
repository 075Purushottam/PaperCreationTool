from django import forms
from .models import PaperDetail
from django.forms import widgets
from .models import UserLogin,ToolLogin
from django.contrib.auth.forms import UserCreationForm

class PaperDetailForm(forms.ModelForm):
    class_name = forms.ChoiceField(choices=())
    school_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'School Name'})
    )
    exam_name = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Exam Name'})
    )
    instructions = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Type Exam Instructions'})
    )
    duration = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': '"How many hours does the paper take?"'})
    )
    marks = forms.IntegerField(
        widget=forms.NumberInput(attrs={'placeholder': '"What is the total number of marks for the paper?"'})
    )
    class Meta:
        model = PaperDetail
        fields = '__all__'
    

    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('choices', [])
        super().__init__(*args, **kwargs)
        self.fields['class_name'].choices = choices


# login register
class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    mobile = forms.CharField(max_length=15, required=True)
    address = forms.CharField(max_length=200, required=True)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'mobile', 'address')




class UserLoginCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = UserLogin
        fields = ['name', 'email', 'mobile', 'address', 'password','confirm_password']

class ToolLoginCreateForm(forms.Form):
    name = forms.CharField(max_length=150)
    email = forms.EmailField()


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
