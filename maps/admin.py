from django.contrib import admin
from django_json_widget.widgets import JSONEditorWidget

from .models import *


@admin.register(HospitalRoute)
@admin.register(TrafficSignal)
class YourModelAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.JSONField: {'widget': JSONEditorWidget},
    }


admin.site.register(TrafficLight)
admin.site.register(Hospital)
