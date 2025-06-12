from django import forms
from .models import Notes, Homework,Todo
from django.forms.widgets import DateTimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Notes Form
class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title', 'description']

# Homework Form with datetime-local widget
class HomeworkForm(forms.ModelForm):
    class Meta:
        model = Homework
        fields = ['subject', 'title', 'description', 'due', 'is_finished']
        widgets = {
            'due': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
        }

class DashboardForm(forms.Form):
    text = forms.CharField(max_length=100,label="Search bar")

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title','is_finished']

from django import forms

class ConversionForm(forms.Form): 
    CHOICES = [('length', 'Length'), ('mass', 'Mass')]
    measurement = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect)

class ConversionLengthForm(forms.Form):
    CHOICE = [('yard', 'Yard'), ('foot', 'Foot')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter The Number'})
    )
    measure1 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICE)
    )
    measure2 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICE)
    )

class ConversionMassForm(forms.Form):
    CHOICE = [('pound', 'Pound'), ('kilogram', 'Kilogram')]
    input = forms.CharField(
        required=False,
        label=False,
        widget=forms.TextInput(attrs={'type': 'number', 'placeholder': 'Enter The Number'})
    )
    measure1 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICE)
    )
    measure2 = forms.CharField(
        label='',
        widget=forms.Select(choices=CHOICE)
    )

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        
class AIAssistantForm(forms.Form):
    question = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': '💬 Ask your AI assistant anything...',
            'class': 'form-control',
        })
    )