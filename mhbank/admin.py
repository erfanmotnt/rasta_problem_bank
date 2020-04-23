from django.contrib import admin
from django.utils import timezone

from .models import Question, Account, Tag, Sub_tag

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['question_maker', 'last_change_date']

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


# admin.site.register(Question)
admin.site.register(Account)

class SubTagInline(admin.TabularInline): #StackedInline
    model = Sub_tag
    extra = 1

class TagAdmin(admin.ModelAdmin):
    inlines = [SubTagInline]


admin.site.register(Tag, TagAdmin)