import json
import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone

from training.models import TrainingPlan, Exercise, ClientTrainingPlan
from users.models import Client


@login_required(login_url='login')
def training_plans(request):
    trainer = request.user.trainer
    plans   = TrainingPlan.objects.filter(trainer=trainer, is_archived=False).prefetch_related('exercises')
    clients = Client.objects.filter(trainer=trainer, is_archive=False)

    return render(request, 'training/training_plan.html', {
        'plans'  : plans,
        'clients': clients,
    })


@login_required(login_url='login')
@require_POST
def create_plan(request):
    trainer = request.user.trainer

    plan = TrainingPlan.objects.create(
        trainer           = trainer,
        plan_name         = request.POST.get('plan_name'),
        goal              = request.POST.get('goal'),
        duration_weeks    = request.POST.get('duration_weeks'),
        days_per_week     = request.POST.get('days_per_week'),
        difficulty_level  = request.POST.get('difficulty_level'),
        short_description = request.POST.get('short_description', ''),
    )

    _save_exercises(request, plan)
    return redirect('training_plans')


@login_required(login_url='login')
def edit_plan(request, plan_id):
    trainer = request.user.trainer
    plan    = get_object_or_404(TrainingPlan, id=plan_id, trainer=trainer)

    if request.method == 'POST':
        plan.plan_name         = request.POST.get('plan_name')
        plan.goal              = request.POST.get('goal')
        plan.duration_weeks    = request.POST.get('duration_weeks')
        plan.days_per_week     = request.POST.get('days_per_week')
        plan.difficulty_level  = request.POST.get('difficulty_level')
        plan.short_description = request.POST.get('short_description', '')
        plan.save()

        plan.exercises.all().delete()
        _save_exercises(request, plan)
        return redirect('training_plans')

    # GET — return plan + exercises as JSON for the edit form
    exercises = list(plan.exercises.order_by('order').values(
        'exercise_name', 'sets', 'reps_duration', 'rest_seconds', 'weight', 'notes'
    ))
    return JsonResponse({
        'id'               : plan.id,
        'plan_name'        : plan.plan_name,
        'goal'             : plan.goal,
        'duration_weeks'   : plan.duration_weeks,
        'days_per_week'    : plan.days_per_week,
        'difficulty_level' : plan.difficulty_level,
        'short_description': plan.short_description,
        'exercises'        : exercises,
    })


@login_required(login_url='login')
def view_plan(request, plan_id):
    trainer = request.user.trainer
    plan    = get_object_or_404(TrainingPlan, id=plan_id, trainer=trainer)

    exercises = list(plan.exercises.order_by('order').values(
        'exercise_name', 'sets', 'reps_duration', 'rest_seconds', 'weight', 'notes'
    ))
    return JsonResponse({
        'id'               : plan.id,
        'plan_name'        : plan.plan_name,
        'goal'             : plan.goal,
        'duration_weeks'   : plan.duration_weeks,
        'days_per_week'    : plan.days_per_week,
        'difficulty_level' : plan.difficulty_level,
        'short_description': plan.short_description,
        'exercises'        : exercises,
    })


@login_required(login_url='login')
def delete_plan(request, plan_id):
    trainer = request.user.trainer
    plan    = get_object_or_404(TrainingPlan, id=plan_id, trainer=trainer)
    plan.delete()
    return redirect('training_plans')


@login_required(login_url='login')
@require_POST
def assign_plan(request, plan_id):
    trainer   = request.user.trainer
    plan      = get_object_or_404(TrainingPlan, id=plan_id, trainer=trainer)
    client_id = request.POST.get('client_id')
    client    = get_object_or_404(Client, id=client_id, trainer=trainer)

    ClientTrainingPlan.objects.create(
        training_plan = plan,
        client        = client,
        assigned_by   = trainer,
        start_date    = timezone.localtime(timezone.now()).date(),
        end_date      = None,
        is_active     = True,
        is_archived   = False,
    )

    return redirect('training_plans')


# ── AI Plan Generator ─────────────────────────────────────────────────────────
@login_required(login_url='login')
@require_POST
def generate_plan_ai(request):
    """
    Receives a JSON body with client context and plan preferences,
    calls OpenAI, returns a structured JSON plan for the frontend to preview.
    The trainer reviews and then saves normally via create_plan.
    """
    try:
        body           = json.loads(request.body)
        goal           = body.get('goal', '')
        difficulty     = body.get('difficulty', '')
        duration_weeks = body.get('duration_weeks', '')
        days_per_week  = body.get('days_per_week', '')
        extra_context  = body.get('extra_context', '').strip()
    except (json.JSONDecodeError, AttributeError):
        return JsonResponse({'error': 'Invalid request body.'}, status=400)

    if not all([goal, difficulty, duration_weeks, days_per_week]):
        return JsonResponse({'error': 'Please fill in goal, difficulty, duration and days/week before generating.'}, status=400)

    # Build a clear, specific prompt
    prompt = f"""You are an expert personal trainer. Generate a training plan with the following requirements:

- Goal: {goal}
- Difficulty: {difficulty}
- Duration: {duration_weeks} weeks
- Training days per week: {days_per_week}
{f'- Additional context: {extra_context}' if extra_context else ''}

Respond ONLY with a valid JSON object in exactly this format, no extra text, no markdown:

{{
  "plan_name": "A descriptive name for this plan",
  "short_description": "One sentence describing what this plan achieves",
  "exercises": [
    {{
      "exercise_name": "Exercise Name",
      "sets": 3,
      "reps_duration": "10-12",
      "rest_seconds": 60,
      "weight": "Bodyweight",
      "notes": "Keep core engaged throughout"
    }}
  ]
}}

Rules:
- Include 5 to 8 exercises appropriate for the goal and difficulty level
- sets must be a number (e.g. 3)
- reps_duration is a string (e.g. "10-12 reps" or "30 seconds")
- rest_seconds is a number in seconds (e.g. 60)
- weight can be empty string if not applicable
- notes should be a practical coaching cue
- Do not include any text outside the JSON object"""

    try:
        import urllib.request

        api_key = os.environ.get('GEMINI_API_KEY', '')
        if not api_key:
            return JsonResponse({'error': 'API key not configured.'}, status=500)

        payload = json.dumps({
            'model': 'gemini-3.6-flash',
            'messages'   : [{'role': 'user', 'content': prompt}],
            'temperature': 0.7,
            'max_completion_tokens': 1500,
        }).encode('utf-8')

        req = urllib.request.Request(
            'https://generativelanguage.googleapis.com/v1beta/openai/chat/completions',
            data    = payload,
            headers = {
                'Content-Type' : 'application/json',
                'Authorization': f'Bearer {api_key}',
            },
            method  = 'POST',
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read().decode('utf-8'))

        raw_text = result['choices'][0]['message']['content'].strip()

        # Strip markdown fences if the model wraps in ```json ... ```
        if raw_text.startswith('```'):
            raw_text = raw_text.split('```')[1]
            if raw_text.startswith('json'):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        plan_data = json.loads(raw_text)

        # Validate expected keys exist
        if 'exercises' not in plan_data or 'plan_name' not in plan_data:
            raise ValueError('Unexpected response structure from AI.')

        return JsonResponse({'success': True, 'plan': plan_data})

    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return JsonResponse({'error': f'OpenAI API error: {e.code} — {error_body}'}, status=502)
    except (json.JSONDecodeError, ValueError) as e:
        return JsonResponse({'error': f'Could not parse AI response: {str(e)}'}, status=502)
    except Exception as e:
        return JsonResponse({'error': f'Unexpected error: {str(e)}'}, status=500)


# ── Helper ────────────────────────────────────────────────────────────────────
def _save_exercises(request, plan):
    names   = request.POST.getlist('exercise_name')
    sets    = request.POST.getlist('sets')
    reps    = request.POST.getlist('reps_duration')
    rests   = request.POST.getlist('rest_seconds')
    weights = request.POST.getlist('weight')
    notes   = request.POST.getlist('notes')

    for i, name in enumerate(names):
        if not name.strip():
            continue
        Exercise.objects.create(
            training_plan = plan,
            exercise_name = name,
            sets          = sets[i]    or 0,
            reps_duration = reps[i]    or '',
            rest_seconds  = rests[i]   or None,
            weight        = weights[i] or '',
            notes         = notes[i]   or '',
            order         = i + 1,
        )