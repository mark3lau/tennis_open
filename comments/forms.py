from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '3'}), required=False)

    class Meta:
        model = Comment
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        initial_message = kwargs.get('initial', {}).get('message')
        super().__init__(*args, **kwargs)
        if initial_message:
            self.fields['message'].initial = initial_message
