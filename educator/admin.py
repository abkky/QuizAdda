from django.contrib import admin
from .models import answers, question, quiz, responser
# Register your models here.
@admin.register(quiz,question,responser,answers)
class UserAdmin(admin.ModelAdmin):
    pass