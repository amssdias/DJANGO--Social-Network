from django import forms

class NewPost(forms.Form):
    post = forms.CharField(widget=forms.Textarea(attrs={'class' : "form-control", 'id' : "exampleFormControlTextarea1", 'rows':"3", 'placeholder': 'New post'}), label='New Post')