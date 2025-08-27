from django.shortcuts import render
from contact.forms import RegisterForm

def register(request):
    form = RegisterForm()
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        
        if form.is_valid():
            form.save()
            form = RegisterForm()
    
    context = {
        'form': form
    }
    
    return render(
        request,
        'contact/register.html',
        context,
    )