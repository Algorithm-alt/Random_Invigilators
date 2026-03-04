from django import forms
from .models import Teacher, ExaminationCenter

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['name', 'email', 'subject']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ExaminationCenterForm(forms.ModelForm):
    class Meta:
        model = ExaminationCenter
        fields = ['name', 'location', 'capacity']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class GenerateAssignmentForm(forms.Form):
    confirm = forms.BooleanField(initial=True, widget=forms.HiddenInput)
