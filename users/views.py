from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import UserRegistrationForm
from django.core.mail import send_mail
from django.conf import settings

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # отправка письма
            send_mail(
                subject='Добро пожаловать!',
                message=f'Привет, {user.email}. Спасибо за регистрацию.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True,
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})
