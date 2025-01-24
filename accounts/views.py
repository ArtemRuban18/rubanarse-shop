from django.shortcuts import render, redirect
from .forms import SignUp
from django.contrib.auth.views import LoginView

def signup(request):
    if request.method == 'POST':
        signup_form = SignUp(request.GET)
        if signup_form.is_valid():
            signup_form.save()
            return redirect(request, 'login', {'signup_form':signup_form})
        else:
            signup_form = SignUp()
    return render(request, 'signup.html', {'signup_form':signup_form}) 