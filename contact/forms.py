from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from contact.models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        widget=forms.FileInput(attrs={'accept': 'image/*'}),
    )
    
    class Meta:
        model = Contact
        fields= ('first_name', 'last_name', 'phone', 'email', 'description', 'category', 'picture',)

    def clean(self):
        cleaned_data = self.cleaned_data
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')
        
        if first_name == last_name:
            self.add_error(
                'last_name',
                ValidationError(
                    'O primeiro nome e o sobrenome não podem ser iguais.',
                    code='invalid_name'
                )
            )
        
        return super().clean()

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        
        if first_name == 'ABC':
            self.add_error(
                'first_name',
                ValidationError(
                    'O nome "ABC" não é permitido.',
                    code='invalid_name'
                )
            )
        
        return first_name

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
    )
    last_name = forms.CharField(
        required=True,
    )
    email = forms.EmailField(
        required=True,
    )
    
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2',)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        
        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError(
                    'Este email já está em uso.',
                    code='invalid_email'
                )
            )
        return email
        