from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.safestring import mark_safe
from datetime import datetime, timedelta, date
import json
from users.models import Client
from scheduling.models import Appointment


@login_required(login_url='login')
def schedule(request):
    trainer = request.user.trainer
    today = timezone.localtime(timezone.now()).date()
    clients = Client.objects.filter(trainer=trainer, is_archive=False)

    appointments       = Appointment.objects.filter(trainer=trainer)
    today_appointments = appointments.filter(appointment_date=today)

    week_start        = today - timedelta(days=today.weekday())
    week_end          = week_start + timedelta(days=6)
    week_appointments = appointments.filter(appointment_date__range=[week_start, week_end])
    confirmed_count   = appointments.filter(is_cancelled=False, is_completed=False).count()

    if request.method == 'POST':
        client_id    = request.POST.get('client')
        session_type = request.POST.get('session_type')
        date_str     = request.POST.get('date')
        time         = request.POST.get('start_time')
        duration     = request.POST.get('duration')
        repeat       = request.POST.get('repeat')
        notes        = request.POST.get('notes')

        Appointment.objects.create(
            trainer          = trainer,
            client           = Client.objects.get(id=client_id),
            session_type     = session_type,
            appointment_date = date_str,
            appointment_time = time,
            duration         = int(duration),
            repeat           = repeat,
            notes            = notes,
        )
        return redirect('schedule')

    COLOR_MAP = {
        'strength_training'   : '#c8102e',
        'hiit_cardio'         : '#2563eb',
        'flexibility_mobility': '#16a34a',
        'weight_loss'         : '#7c3aed',
        'consultation'        : '#ea580c',
    }

    events = []
    for a in appointments:
        start_dt = datetime.combine(a.appointment_date, a.appointment_time)
        end_dt   = start_dt + timedelta(minutes=a.duration)

        event = {
            'id'   : a.id,
            'title': f"{a.client.first_name} {a.client.last_name}",
            'start': start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'end'  : end_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            'color': COLOR_MAP.get(a.session_type, '#c8102e'),
            'extendedProps': {
                'id'          : a.id,
                'client_id'   : a.client.id,                  # ← new
                'client'      : f"{a.client.first_name} {a.client.last_name}",
                'session_type': a.session_type,                # ← raw value for <select>
                'session_type_display': a.get_session_type_display(),
                'notes'       : a.notes or '',
                'repeat'      : a.repeat,                      # ← new
                'duration'    : a.duration,                    # ← new
                'status'      : 'Completed' if a.is_completed else 'Cancelled' if a.is_cancelled else 'Confirmed',
            }
        }

        if a.repeat == 'weekly':
            event['rrule'] = {
                'freq'   : 'weekly',
                'dtstart': start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            event['duration'] = f'{a.duration // 60:02d}:{a.duration % 60:02d}:00'

        elif a.repeat == 'biweekly':
            event['rrule'] = {
                'freq'    : 'weekly',
                'interval': 2,
                'dtstart' : start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            event['duration'] = f'{a.duration // 60:02d}:{a.duration % 60:02d}:00'

        elif a.repeat == 'monthly':
            event['rrule'] = {
                'freq'   : 'monthly',
                'dtstart': start_dt.strftime('%Y-%m-%dT%H:%M:%S'),
            }
            event['duration'] = f'{a.duration // 60:02d}:{a.duration % 60:02d}:00'

        events.append(event)

    # mark_safe prevents Django from HTML-escaping quotes in the JSON,
    # so {{ appointments_json }} in a <script> tag renders as valid JS.
    appointments_json = mark_safe(json.dumps(events))

    return render(request, 'scheduling/schedule.html', {
        'clients'           : clients,
        'today_appointments': today_appointments,
        'today'             : today,
        'week_count'        : week_appointments.count(),
        'today_count'       : today_appointments.count(),
        'confirmed_count'   : confirmed_count,
        'appointments_json' : appointments_json,
    })

@login_required(login_url='login')
def edit_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk, trainer=request.user.trainer)
    if request.method == 'POST':
        appointment.client           = Client.objects.get(id=request.POST.get('client'))
        appointment.session_type     = request.POST.get('session_type')
        appointment.appointment_date = request.POST.get('date')
        appointment.appointment_time = request.POST.get('start_time')
        appointment.duration         = int(request.POST.get('duration'))
        appointment.repeat           = request.POST.get('repeat')
        appointment.notes            = request.POST.get('notes')
        appointment.save()
    return redirect('schedule')


@login_required(login_url='login')
def delete_appointment(request, pk):
    if request.method == 'POST':
        Appointment.objects.filter(id=pk, trainer=request.user.trainer).delete()
    return redirect('schedule')