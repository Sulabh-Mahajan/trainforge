import json
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import Client, Trainer
from training.models import TrainingPlan, Exercise
from progress.models import ClientExerciseProgress


@login_required
def progress_view(request):
    trainer = request.user.trainer
    clients = Client.objects.filter(trainer=trainer, is_archive=False).order_by('first_name')
    return render(request, 'progress/progress.html', {'clients': clients})


@login_required
def search_clients(request):
    q       = request.GET.get('q', '').strip()
    trainer = request.user.trainer
    clients = Client.objects.filter(
        trainer=trainer, is_archive=False
    ).filter(
        first_name__icontains=q
    ) | Client.objects.filter(
        trainer=trainer, is_archive=False
    ).filter(last_name__icontains=q)

    data = [{
        'id'      : c.id,
        'name'    : f'{c.first_name} {c.last_name}',
        'initials': f'{c.first_name[:1]}{c.last_name[:1]}',
        'meta'    : f'Age {c.age} · {c.get_sex_display()}' if c.age else '',
    } for c in clients[:10]]
    return JsonResponse(data, safe=False)


@login_required
def client_plans(request, client_id):
    trainer = request.user.trainer
    client  = Client.objects.get(pk=client_id, trainer=trainer)
    plans   = TrainingPlan.objects.filter(client=client)

    data = [{
        'id'            : p.id,
        'name'          : p.name,
        'goal'          : p.goal if hasattr(p, 'goal') else '',
        'exercise_count': p.exercise_set.count(),
    } for p in plans]
    return JsonResponse(data, safe=False)


@login_required
def plan_exercises(request, plan_id, client_id):
    exercises = Exercise.objects.filter(training_plan_id=plan_id).order_by('order')

    data = []
    for ex in exercises:
        progress_qs = ClientExerciseProgress.objects.filter(
            exercise_id=ex.id, client_id=client_id
        ).order_by('progress_date')

        data.append({
            'id'           : ex.id,
            'exercise_name': ex.exercise_name,
            'sets'         : ex.sets,
            'reps_duration': ex.reps_duration,
            'weight'       : ex.weight or '',
            'progress'     : [
                {'date': str(p.progress_date), 'value': p.benchmark_value}
                for p in progress_qs
            ],
        })
    return JsonResponse(data, safe=False)


@login_required
def log_progress(request):
    if request.method != 'POST':
        return JsonResponse({'success': False})
    body            = json.loads(request.body)
    exercise_id     = body.get('exercise_id')
    client_id       = body.get('client_id')
    benchmark_value = body.get('benchmark_value')
    progress_date   = body.get('progress_date')
    notes           = body.get('notes', '')

    ex = Exercise.objects.get(pk=exercise_id)
    ClientExerciseProgress.objects.create(
        exercise_id     = exercise_id,
        client_id       = client_id,
        benchmark_value = benchmark_value,
        progress_date   = progress_date,
        notes           = notes,
        updated_by      = request.user,
    )
    return JsonResponse({'success': True, 'plan_id': ex.training_plan_id})