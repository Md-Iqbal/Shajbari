from django import forms


from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'input', 'placeholder': 'example@gmail.com'}),
            'name': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Your Name Here'}),
            'subject': forms.TextInput(attrs={'class': 'input', 'placeholder': 'Subject of your message'}),
            'message': forms.Textarea(attrs={'class': 'input', 'placeholder': 'Your Message Here'}),
        }

class SearchForm(forms.Form):
    query=forms.CharField(max_length=100)