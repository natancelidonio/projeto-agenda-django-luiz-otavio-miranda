from django import forms
from django.core.exceptions import ValidationError
from contact.models import Contact

class ContactForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'classe-a classe-b',
                'placeholder': 'Digite seu nome aqui...'
            }
        ),
        label='Primeiro Nome',
        help_text='Digite seu primeiro nome',
    )
    
        
    class Meta:
        model = Contact
        fields= ('first_name', 'last_name', 'phone',)
        # widgets = {
        #     'first_name': forms.TextInput(
        #         attrs={
        #             'class': 'classe-a classe-b',
        #             'placeholder': 'Digite seu nome'
        #         }
        #     ),
        # }

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