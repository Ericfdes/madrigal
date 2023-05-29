from django import forms
from django.forms import formset_factory
from django.forms import formset_factory, inlineformset_factory

class WorkExperienceForm(forms.Form):
    emp_position = forms.CharField(label='Work Title:')
    emp_StartMonth = forms.CharField(widget=forms.TextInput(attrs={'type': 'month', 'class':'col-md-4'}), label='Start Month:')
    emp_StartYear = forms.IntegerField(label='Start Year:')
    emp_EndMonth = forms.CharField(widget=forms.TextInput(attrs={'type': 'month'}), label='End Month:')
    emp_EndYear = forms.IntegerField(label='End Year:')
    emp_description = forms.CharField(widget=forms.Textarea(), label="Work Description:")


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.IntegerField):
                field.widget.attrs['class'] = 'form-control col-md-4'
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'

class EducationForm(forms.Form):
    school_name = forms.CharField(label='School Name:')
    school_location = forms.CharField(label='School Location:')
    degree = forms.CharField(label='Degree:')
    field_of_study = forms.CharField(label='Field of Study:')
    startYear = forms.IntegerField(label='Start Year:')
    endYear = forms.IntegerField(label='End Year:')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.IntegerField):
                field.widget.attrs['class'] = 'form-control col-md-4'
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'

class SkillForm(forms.Form):
    skillset = forms.CharField(label='Skill Set:',widget=forms.TextInput(attrs={'placeholder':'Ex: Languages'}))
    skills = forms.CharField(label='Skills:', widget=forms.TextInput(attrs={'placeholder':'List out your skills separated by a comma'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, forms.CharField):
                field.widget.attrs['class'] = 'form-control'



WorkExperienceFormSet = formset_factory(WorkExperienceForm, extra=1)
EducationFormSet = formset_factory(EducationForm, extra=1)
SkillsFormSet = formset_factory(SkillForm, extra=1)