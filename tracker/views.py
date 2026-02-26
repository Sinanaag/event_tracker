from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django import forms

from .models import Event, Task, Attendee, EventNote
import json


# -------------------------
# Custom Register Form
# -------------------------

class CustomRegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


# -------------------------
# Dashboard
# -------------------------

@login_required
def dashboard(request):
    events = Event.objects.filter(user=request.user)

    planning_events = events.filter(status='Planning')
    in_progress_events = events.filter(status='In Progress')
    completed_events = events.filter(status='Completed')
    cancelled_events = events.filter(status='Cancelled')

    context = {
        'planning': planning_events,
        'in_progress': in_progress_events,
        'completed': completed_events,
        'cancelled': cancelled_events,
        'total': events.count(),
        'in_progress_count': in_progress_events.count(),
        'completed_count': completed_events.count(),
    }

    return render(request, 'dashboard.html', context)


# -------------------------
# Update Status (Drag & Drop)
# -------------------------

@login_required
@csrf_exempt
def update_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            event_id = data.get("event_id")
            new_status = data.get("new_status")

            event = Event.objects.get(id=event_id, user=request.user)
            event.status = new_status
            event.save()
            return JsonResponse({"success": True})
        except Event.DoesNotExist:
            return JsonResponse({"success": False, "error": "Event not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


# -------------------------
# Add Event
# -------------------------

@login_required
def add_event(request):
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        date = request.POST.get("date")
        time = request.POST.get("time")
        location = request.POST.get("location")
        priority = request.POST.get("priority", "Medium")
        expected_attendees = request.POST.get("expected_attendees", 0)
        budget = request.POST.get("budget")

        event = Event.objects.create(
            user=request.user,
            name=name,
            description=description,
            date=date,
            time=time if time else None,
            location=location,
            priority=priority,
            expected_attendees=int(expected_attendees) if expected_attendees else 0
        )
        
        if budget:
            event.budget = budget
            event.save()

        return redirect('event_detail', id=event.id)

    return render(request, 'add_event.html')


# -------------------------
# Event Detail
# -------------------------

from django.shortcuts import get_object_or_404

@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id, user=request.user)
    tasks = event.tasks.all()
    attendees = event.attendees.all()
    notes = event.notes.all()

    return render(request, 'event_detail.html', {
        'event': event,
        'tasks': tasks,
        'attendees': attendees,
        'notes': notes,
    })


# -------------------------
# Add Task
# -------------------------

@login_required
def add_task(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        assigned_to = request.POST.get("assigned_to")
        due_date = request.POST.get("due_date")

        Task.objects.create(
            event=event,
            title=title,
            description=description,
            assigned_to=assigned_to,
            due_date=due_date if due_date else None
        )

        return redirect('event_detail', id=event_id)

    return render(request, 'add_task.html', {'event': event})


# -------------------------
# Update Task Status
# -------------------------

@login_required
@csrf_exempt
def update_task_status(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            task_id = data.get("task_id")
            new_status = data.get("new_status")

            task = Task.objects.get(id=task_id)
            task.status = new_status
            task.save()
            return JsonResponse({"success": True})
        except Task.DoesNotExist:
            return JsonResponse({"success": False, "error": "Task not found"}, status=404)
        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)


# -------------------------
# Add Attendee
# -------------------------

@login_required
def add_attendee(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        Attendee.objects.create(
            event=event,
            name=name,
            email=email,
            phone=phone
        )

        return redirect('event_detail', id=event_id)

    return render(request, 'add_attendee.html', {'event': event})


# -------------------------
# Register
# -------------------------

def register(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = CustomRegisterForm()

    return render(request, 'register.html', {'form': form})