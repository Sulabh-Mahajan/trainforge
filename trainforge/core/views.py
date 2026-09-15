from datetime import timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from users.models import Client
from training.models import TrainingPlan, ClientTrainingPlan, Exercise
from scheduling.models import Appointment
from progress.models import ClientExerciseProgress
from django.db.models import Min

def home(request):
    return render(request, 'core/home_page.html')


@login_required
def dashboard(request):
    try:
        trainer = request.user.trainer
    except:
        from users.models import Trainer, Subscription
        subscription = Subscription.objects.filter(plan_name='Free').first()
        Trainer.objects.create(
            user                  = request.user,
            experience            = 'less_than_1',
            doj                   = timezone.localdate(),
            primary_certification = 'other',
            subscription          = subscription,
        )
        trainer = request.user.trainer

    today   = timezone.localdate()
    now     = timezone.now()

    clients = Client.objects.filter(trainer=trainer, is_archive=False)

    active_clients = clients.count()
    active_plans   = TrainingPlan.objects.filter(
        trainer=trainer,
        is_archived=False,
    ).count()

    week_start    = today - timedelta(days=today.weekday())
    sessions_week = Appointment.objects.filter(
        trainer=trainer,
        appointment_date__gte=week_start,
        appointment_date__lte=today,
        is_cancelled=False,
    ).count()

    todays_appointments = Appointment.objects.filter(
        trainer=trainer,
        appointment_date=today,
        is_cancelled=False,
    ).select_related('client').order_by('appointment_time')


    next_session_dates = Appointment.objects.filter(
        trainer=trainer,
        appointment_date__gte=today,
        is_cancelled=False,
        is_completed=False,
    ).values('client').annotate(next_date=Min('appointment_date'))

    next_session_map = {}
    for entry in next_session_dates:
        appt = Appointment.objects.filter(
            trainer=trainer,
            client_id=entry['client'],
            appointment_date=entry['next_date'],
            is_cancelled=False,
            is_completed=False,
        ).order_by('appointment_time').first()
        if appt:
            next_session_map[entry['client']] = appt

    # Attach next session directly to each client object
    for client in clients:
        client.next_session = next_session_map.get(client.id)

    return render(request, 'core/dashboard.html', {
        'today'              : today.strftime('%A, %d %B %Y'),
        'now'                : now,
        'clients'            : clients,
        'active_clients'     : active_clients,
        'active_plans'       : active_plans,
        'sessions_week'      : sessions_week,
        'todays_appointments': todays_appointments,
        'next_session_map'   : next_session_map,   # ← this was missing
    })


@login_required
def add_client(request):
    if request.method == 'POST':
        Client.objects.create(
            trainer               = request.user.trainer,
            first_name            = request.POST.get('first_name'),
            last_name             = request.POST.get('last_name'),
            email                 = request.POST.get('email'),
            phone                 = request.POST.get('phone'),
            sex                   = request.POST.get('sex'),
            age                   = request.POST.get('age'),
            height                = request.POST.get('height'),
            weight                = request.POST.get('weight'),
            initial_fitness_level = request.POST.get('initial_fitness_level'),
        )
        return redirect(reverse('dashboard') + '?client_added=true')
    return redirect(reverse('dashboard'))


@login_required
def client_detail(request, client_id):
    trainer = request.user.trainer
    client  = get_object_or_404(Client, id=client_id, trainer=trainer)

    # All plans this trainer has (not archived) — for the assign section
    plans = TrainingPlan.objects.filter(trainer=trainer, is_archived=False)

    # All assignments for this client, newest first
    assignments = (
        ClientTrainingPlan.objects
        .filter(client=client, assigned_by=trainer)
        .select_related('training_plan')
        .order_by('-assigned_at')
    )

    # Build enriched list with per-exercise progress logs
    enriched = []
    for assignment in assignments:
        exercises_with_progress = []
        for exercise in assignment.training_plan.exercises.all():
            progress_logs = (
                ClientExerciseProgress.objects
                .filter(client=client, exercise=exercise)
                .order_by('-progress_date')
            )
            exercises_with_progress.append({
                'exercise'     : exercise,
                'progress_logs': progress_logs,
            })
        enriched.append({
            'assignment': assignment,
            'exercises' : exercises_with_progress,
        })

    return render(request, 'users/client_detail.html', {
        'client'  : client,
        'enriched': enriched,
        'plans'   : plans,
    })


@login_required
def end_plan(request, assignment_id):
    if request.method == 'POST':
        trainer    = request.user.trainer
        assignment = get_object_or_404(
            ClientTrainingPlan,
            id=assignment_id,
            assigned_by=trainer,
        )
        assignment.end_date  = timezone.localdate()
        assignment.is_active = False
        assignment.save()
    return redirect(request.POST.get('next', reverse('dashboard')))


@login_required
def add_progress(request, exercise_id, client_id):
    if request.method == 'POST':
        trainer  = request.user.trainer
        client   = get_object_or_404(Client, id=client_id, trainer=trainer)
        exercise = get_object_or_404(Exercise, id=exercise_id)
        ClientExerciseProgress.objects.create(
            client          = client,
            exercise        = exercise,
            updated_by      = trainer,
            benchmark_value = request.POST.get('benchmark_value'),
            progress_date   = request.POST.get('progress_date') or timezone.localdate(),
            notes           = request.POST.get('notes', ''),
        )
    return redirect(reverse('client_detail', args=[client_id]))


@login_required
def assign_plan_to_client(request, client_id):
    if request.method == 'POST':
        trainer = request.user.trainer
        client  = get_object_or_404(Client, id=client_id, trainer=trainer)
        plan_id = request.POST.get('plan_id')
        plan    = get_object_or_404(TrainingPlan, id=plan_id, trainer=trainer)

        ClientTrainingPlan.objects.create(
            client        = client,
            training_plan = plan,
            assigned_by   = trainer,
            start_date    = timezone.localdate(),
            is_active     = True,
        )
    return redirect(reverse('client_detail', args=[client_id]) + '?plan_assigned=true')


@login_required
def edit_client(request, client_id):
    if request.method == 'POST':
        trainer = request.user.trainer
        client  = get_object_or_404(Client, id=client_id, trainer=trainer)
        client.first_name            = request.POST.get('first_name')
        client.last_name             = request.POST.get('last_name')
        client.email                 = request.POST.get('email')
        client.phone                 = request.POST.get('phone', '')
        client.sex                   = request.POST.get('sex')
        client.age                   = request.POST.get('age')
        client.height                = request.POST.get('height')
        client.weight                = request.POST.get('weight')
        client.initial_fitness_level = request.POST.get('initial_fitness_level', '')
        client.save()
    return redirect(reverse('client_detail', args=[client_id]))

@login_required
def archive_client(request, client_id):
    if request.method == 'POST':
        trainer = request.user.trainer
        client  = get_object_or_404(Client, id=client_id, trainer=trainer)
        client.is_archive = True
        client.save()
    return redirect(reverse('dashboard'))