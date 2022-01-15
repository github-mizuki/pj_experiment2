from django.contrib import admin
from .models import MainTask, Log, SubTask
# Register your models here.

admin.site.register(
    [MainTask, Log, SubTask]
)