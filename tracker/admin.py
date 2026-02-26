from django.contrib import admin
from .models import Event, Task, Attendee, EventNote

admin.site.register(Event)
admin.site.register(Task)
admin.site.register(Attendee)
admin.site.register(EventNote)