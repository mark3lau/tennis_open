from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)
    
    class Meta:
        model = Comment
        fields = ('message',)