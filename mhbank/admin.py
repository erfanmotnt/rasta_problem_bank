from django.contrib import admin

from .models import Question, Account

admin.site.register(Question)
admin.site.register(Account)
