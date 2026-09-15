from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Trainer, TrainerSpecialization, Subscription

from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == 'POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            return render(request, 'users/login.html', {
                'errors': 'Please enter your email and password.'
            })

        # Django uses username to authenticate, we set username = email at registration
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            # Redirect admin/superuser to admin panel
            if user.is_staff:
                return redirect(reverse('admin:index'))

            # Redirect trainer to dashboard
            return redirect(reverse('dashboard'))

        else:
            return render(request, 'users/login.html', {
                'errors': 'Invalid email or password. Please try again.'
            })

    return render(request, 'users/login.html')


def register(request):
    if request.method == 'POST':

        first_name      = request.POST.get('first_name')
        last_name       = request.POST.get('last_name')
        email           = request.POST.get('email')
        phone           = request.POST.get('phone')
        password        = request.POST.get('password')
        experience      = request.POST.get('experience')
        certification   = request.POST.get('certification')
        specializations = request.POST.getlist('specializations')
        plan            = request.POST.get('plan')

        # Validation
        if not all([first_name, last_name, email, password, experience]):
            return render(request, 'users/registration.html', {
                'errors'   : 'Please fill in all required fields.',
                'form_data': request.POST
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'users/registration.html', {
                'errors'   : 'An account with this email already exists.',
                'form_data': request.POST
            })

        if len(password) < 8:
            return render(request, 'users/registration.html', {
                'errors'   : 'Password must be at least 8 characters.',
                'form_data': request.POST
            })

        try:
            subscription = Subscription.objects.get(plan_name=plan)
        except Subscription.DoesNotExist:
            return render(request, 'users/registration.html', {
                'errors'   : 'Invalid plan selected.',
                'form_data': request.POST
            })

        # 1. Create auth_user
        user = User.objects.create_user(
            username   = email,
            email      = email,
            password   = password,
            first_name = first_name,
            last_name  = last_name,
        )

        # 2. Create trainer profile
        trainer = Trainer.objects.create(
            user                  = user,
            experience            = experience,
            primary_certification = certification,
            subscription          = subscription,
            doj                   = timezone.now().date(),
        )

        # 3. Create specializations
        for spec in specializations:
            TrainerSpecialization.objects.create(
                trainer        = trainer,
                specialization = spec,
            )

        return redirect(reverse('login') + '?registered=true')

    return render(request, 'users/registration.html')