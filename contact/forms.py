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
        # cleaned_data = self.cleaned_data
        self.add_error(
            'first_name',
            ValidationError(
                'Mensagem de Erro lero lero',
                code='invalid'
            )
        )
        return super().clean()
    