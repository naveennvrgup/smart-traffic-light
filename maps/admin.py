from django.contrib import admin
from .models import *
from django.db import models
from django_json_widget.widgets import JSONEditorWidget

@admin.register(TrafficSignal)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(TrafficLight)
admin.site.register(Hospital)