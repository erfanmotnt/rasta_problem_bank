from django.contrib import admin
from django import forms
from django.utils import timezone

from .models import Question, Account, Tag, Sub_tag
from .forms import QuestionForm, AccountForm

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields = ['name', 'level', 'verification_status', 'text', 'answer', 'source', 'events',
     'appropriate_grades_min', 'appropriate_grades_max', 'tags', 'sub_tags', 'question_maker', 'last_change_date']
    readonly_fields = ['question_maker', 'last_change_date']
    
    list_display = ('name', 'question_maker', 'last_change_date')
    list_filter = ['verification_status', 'question_maker']
    form = QuestionForm
    #events only for admin ...
    #vertify only for mentors and admin
    #all defualt saved for each users
    def save_model(self, request, obj, form, change):
        if not change:
            obj.question_maker = request.user.account

        obj.last_change_date = timezone.localtime()
        obj.save()


    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True if request.user.is_superuser or obj is None else request.user.account.question_set.filter(
            id=obj.id).exists()

    def has_change_permission(self, request, obj=None):
        return True


class AccountAdmin(admin.ModelAdmin):
    form = AccountForm

# admin.site.register(Question)
admin.site.register(Account, AccountAdmin)

class SubTagInline(admin.TabularInline): #StackedInline
    model = Sub_tag
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [SubTagInline]
    
class Sub_tagAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True


admin.site.register(Tag, TagAdmin)
admin.site.register(Sub_tag, Sub_tagAdmin)