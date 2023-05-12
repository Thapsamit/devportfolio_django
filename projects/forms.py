from django.forms import ModelForm

from django import forms
from .models import Project,Review


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title','project_image','description','source_link','demo_link','tags']
        # below we are defining the type for the fields
        widgets = {
            'tags':forms.CheckboxSelectMultiple()
        }
    def __init__(self,*args,**kwargs):
        super(ProjectForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Project Title'}) # defining the type of class we need for title
        # self.fields['description'].widget.attrs.update({'class':'input'})



class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value','body']
        # below we are defining the type for the fields
        
        labels = {'value':'Place your vote','body':'Add a Comment with your vote'}

        widgets = {
            'tags':forms.CheckboxSelectMultiple()
        }
    def __init__(self,*args,**kwargs):
        super(ReviewForm,self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
        # self.fields['title'].widget.attrs.update({'class':'input','placeholder':'Add Project Title'}) # defining the type of class we need for title
        # self.fields['description'].widget.attrs.update({'class':'input'})


