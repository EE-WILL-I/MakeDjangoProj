from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect

from event.form import UserForm, UsersForm


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


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
