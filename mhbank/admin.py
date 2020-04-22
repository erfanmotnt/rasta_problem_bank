from django.contrib import admin

from .models import Question, Account


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    readonly_fields = ['question_maker']

    def save_model(self, request, obj, form, change):
        if not change:
            obj.question_maker = request.user.account
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
