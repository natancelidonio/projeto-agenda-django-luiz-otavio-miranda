from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from contact.models import Contact

class ContactForm(forms.ModelForm):
    picture = forms.ImageField(
        required=False,
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
                    'Este email já está em uso. Digite outro email.',
                    code='invalid_email'
                )
            )
        return email

class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=30,
        required=True,
        help_text='Obrigatório. 30 caracteres ou menos.',
        error_messages={
            'min_length': 'O primeiro nome deve ter no mínimo 2 letras.',
        }
    )
    
    last_name = forms.CharField(
        min_length=2,
        max_length=150,
        required=True,
        help_text='Obrigatório. 150 caracteres ou menos.',
    )
    
    password1 = forms.CharField(
    label='Password',
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    help_text=password_validation.password_validators_help_text_html(),
    required=False,
    )
    
    password2 = forms.CharField(
    label='Password',
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    help_text=password_validation.password_validators_help_text_html(),
    required=False,
    )
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Este email já está em uso. Digite outro email.',
                        code='invalid_email'
                    )
                )
        return email
    
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        
        password = cleaned_data.get('password1')
        
        if password:
            user.set_password(password)
        
        if commit:
            user.save()
        
        return user
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError(
                        'As senhas não são iguais. Tente novamente.',
                        code='invalid_password'
                    )
                )
        
        return super().clean()
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        
        if password1:
           try:
               password_validation.validate_password(password1)
           except ValidationError as errors:
               self.add_error(
                   'password1',
                   ValidationError(
                       errors,
                       code='invalid_password'
                   )
               )
        
        return password1