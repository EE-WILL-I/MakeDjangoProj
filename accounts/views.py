from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from accounts.forms import SignupForm1, SignupForm2
from event.form import UserForm, UsersForm



@login_required
@transaction.atomic
def update_users(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        users_form = UsersForm(request.POST, instance=request.user.users)
        if user_form.is_valid() and users_form.is_valid():
            user_form.save()
            users_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('settings:users')
        else:
            messages.error(request, ('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        users_form = UsersForm(instance=request.user.users)
    return render(request, 'registration/signup.html', {
        'user_form': user_form,
        'users_form': users_form
    })

@login_required
@transaction.atomic
def signup(request):
    if request.method == 'POST':
        form1 = SignupForm1(request.POST, instance=request.user)
        form2 = SignupForm2(request.POST, instance=request.user.users)
        if form1.is_valid() and form2.is_valid():
            # save form in the memory not in database
            user1 = form1.save(commit=False)
            user2 = form2.save()
            user1.save()
            user2.save()
            messages.success(request, ('Your profile was successfully updated!'))
            return redirect('index.html')
    else:
        form1 = SignupForm1()
        form2 = SignupForm2()
    return render(request, 'registration/signup.html', {
        'form1': form1,
        'form2': form2
    })


