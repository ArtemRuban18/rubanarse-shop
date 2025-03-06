from django.shortcuts import render, redirect
from .forms import SignUp, CustomPasswordResetForm

def signup(request):
    """
    Views for user registration.

    If sigup_form is valid, create new user and redirect to login page.

    Context:
        - signup_form: form for user registration
    Templates:
        -signup.html
    """
    if request.method == 'POST':
        signup_form = SignUp(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            return redirect('login')
    else:
        signup_form = SignUp()
    return render(request, 'signup.html', {'signup_form':signup_form})

def password_reset(request):
    """
    Views for password reset

    If password_reset is valid send email with link to reset password.

    Context:
        - password_reset_form: form for password reset
    Templates:
        - password_reset.html
    """
    if request.method == 'POST':
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            password_reset_form.save(request = request)
            return redirect('password_reset_done')
    else:
        password_reset_form = CustomPasswordResetForm()
    return render(request, 'password_reset.html', {'password_reset_form':password_reset_form})