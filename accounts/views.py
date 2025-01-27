from django.shortcuts import render, redirect
from .forms import SignUp, CustomPasswordChangeForm, CustomPasswordResetForm
from django.contrib.auth.decorators import login_required

def signup(request):
    if request.method == 'POST':
        signup_form = SignUp(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            return redirect('login')
    else:
        signup_form = SignUp()
    return render(request, 'signup.html', {'signup_form':signup_form})

@login_required
def password_change(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.POST, user = request.user)
        if password_change_form.is_valid():
            password_change_form.save()
            return redirect('password_change_done')
    else:
        password_change_form = CustomPasswordChangeForm(user = request.user)
    return render(request, 'password_change.html', {'password_change_form':password_change_form})


def password_reset(request):
    if request.method == 'POST':
        password_reset_form = CustomPasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            password_reset_form.save()
            return redirect('password_reset_done')
    else:
        password_reset_form = CustomPasswordResetForm()
    return render(request, 'password_reset.html', {'password_reset_form':password_reset_form})