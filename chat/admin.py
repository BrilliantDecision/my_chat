from django.contrib import admin
from .models import Online
# Register your models here.


@admin.register(Online)
class OnlineAdmin(admin.ModelAdmin):
    pass
