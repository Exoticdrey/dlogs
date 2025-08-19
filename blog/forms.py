from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'text']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'required': True
            }),
            'text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here...',
                'rows': 5,
                'required': True
            })
        }
        labels = {
            'name': 'Name',
            'text': 'Comment'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        return name

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if len(text) < 5:
            raise forms.ValidationError('Comment must be at least 10 characters long.')
        return text


# ✅ Add this below your CommentForm
class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search blog posts...'
        })
    )
