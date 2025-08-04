from django import forms
from .models import * 

class BookForm(forms.ModelForm):
    class Meta:
        model = BookModel
        fields = '__all__'


class MemberForm(forms.ModelForm):
    class Meta:
        model = MemberModel
        fields = '__all__'


class IssueForm(forms.ModelForm):
    class Meta:
        model = IssueModel
        fields = ['book','member']


class MemberSearchForm(forms.Form):
    query = forms.CharField(label='Search Member' , required=False)

class BookSearchForm(forms.Form):
    query = forms.CharField(label='Search Book' , required=False)