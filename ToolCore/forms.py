from django import forms
from .models import PaperDetail
from django.forms import widgets

class PaperDetailForm(forms.ModelForm):
    class_name = forms.ChoiceField(choices=())
    instructions = forms.TimeField(
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
