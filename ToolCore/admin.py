from django.contrib import admin
from .models import UserLogin, ToolLogin, Paper
admin.site.register(UserLogin)
admin.site.register(ToolLogin)
admin.site.register(Paper)
