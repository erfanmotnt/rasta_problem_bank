from django.contrib import admin
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
import datetime
from .models import Question, Account, Tag, Sub_tag, Event, Source, Hardness, Answer, Comment
from .forms import QuestionForm, AccountForm, HardnessForm

# admin.site.register(Account)
# admin.site.register(Tag)
# admin.site.register(Sub_tag)
# admin.site.register(Event)
# admin.site.register(Source)
# admin.site.register(Hardness)
#
class HardnessInline(admin.StackedInline):
    model = Hardness
    form = HardnessForm

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields_types = {
        'a': ['name', ('verification_status', 'verification_comment'), 'text',
         'source', ('tags', 'sub_tags'), 'question_maker',
              ('publish_date')],
        's': ['name', ('verification_status', 'verification_comment'), 'text',
         'source', 'events', ('tags', 'sub_tags'), 'question_maker',
              ('publish_date')]
    }
    readonly_fields_types = {
        'a': ['question_maker', 'publish_date', 'events', 'verification_status', 'verification_comment'],
        's': ['question_maker', 'publish_date']
    }

    fields = fields_types['s']
    readonly_fields = readonly_fields_types['s']

    list_display = ('name', 'verification_status', 'question_maker')
    list_filter = ['verification_status', 'question_maker']
    form = QuestionForm
    inlines = (HardnessInline,)

    # all defualt saved for each users
    def save_model(self, request, obj, form, change):
        print(obj.text.encode())
        if not change:
            obj.question_maker = request.user.account
            obj.publish_date = timezone.localtime()

        #if obj.question_maker.role == 'a': request.user.account.role
        #    obj.verification_status = 'w'

        #obj.change_date = timezone.localtime()
        obj.save()

    def add_view(self, request, form_url='', extra_context=None):
        if request.user.is_anonymous:
            return False
        if request.user.account.role == 'a':
            self.fields = self.fields_types['a']
        else:
            self.fields = self.fields_types['s']
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_anonymous:
            return False
        if request.user.account.role == 'a':
            self.readonly_fields = self.readonly_fields_types['a']
            self.fields = self.fields_types['s']
        else:
            self.readonly_fields = self.readonly_fields_types['s']
            self.fields = self.fields_types['s']

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def get_form(self, request, obj=None, **kwargs):
        form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        if request.user.is_anonymous:
            return form

        if(obj is None and request.user.account.question_set.exists() > 0):
            #form.base_fields['level'].initial = request.user.account.question_set.latest('publish_date').level
            form.base_fields['source'].initial = request.user.account.question_set.latest('publish_date').source
            if request.user.account.role != 'a':
                form.base_fields['events'].initial = request.user.account.question_set.latest('publish_date').events.all()
            #form.base_fields['appropriate_grades_min'].initial = request.user.account.question_set.latest('publish_date').appropriate_grades_min
            #form.base_fields['appropriate_grades_max'].initial = request.user.account.question_set.latest('publish_date').appropriate_grades_max
            form.base_fields['tags'].initial = request.user.account.question_set.latest('publish_date').tags.all()
            form.base_fields['sub_tags'].initial = request.user.account.question_set.latest('publish_date').sub_tags.all()

        return form

    def has_add_permission(self, request):
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        return True if request.user.is_superuser or obj is None else request.user.account.question_set.filter(
            id=obj.id).exists()

    def has_change_permission(self, request, obj=None):
        if request.user.is_anonymous:
            return False
        return True if request.user.is_superuser or request.user.account.role == 'm' or obj is None else request.user.account.question_set.filter(
            id=obj.id).exists()

class AccountAdmin(admin.ModelAdmin):
    
    list_display = ('user', 'contribution_rate', 'numberOfAdds')
    form = AccountForm

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.is_anonymous:
            return False
        if request.user.account.role == 'a':
            self.fields = ['user','first_name', 'last_name', 'role', 'scientific_rate', 'contribution_rate']
        else:
            self.fields = ['user', 'role', 'first_name', 'last_name', 'phone_number', 'email', 'scientific_rate', 'contribution_rate']
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )



    def has_view_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True


# admin.site.register(Question)
admin.site.register(Account, AccountAdmin)


class SubTagInline(admin.TabularInline):  # StackedInline
    model = Sub_tag
    extra = 1


class TagAdmin(admin.ModelAdmin):
    inlines = [SubTagInline]


class Sub_tagAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return True

class AccoutInline(admin.StackedInline):
    model = Account
    form = AccountForm

class UserAdmin(BaseUserAdmin):
    inlines=(AccoutInline,)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        if obj is None:
            return True
        return request.user.is_superuser

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Sub_tag, Sub_tagAdmin)
admin.site.register(Source)
admin.site.register(Event)
admin.site.register(Answer)
admin.site.register(Comment)
