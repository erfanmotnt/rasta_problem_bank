from django.contrib import admin
from django import forms
from django.utils import timezone

from .models import Question, Account, Tag, Sub_tag
from .forms import QuestionForm, AccountForm


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    fields_types = {
        'a' : ['name', 'level', 'text', 'answer', 'source',
            'appropriate_grades_min', 'appropriate_grades_max', 'tags', 'sub_tags', 'question_maker', 'last_change_date'],
        's' :  ['name', 'level', 'verification_status', 'text', 'answer', 'source', 'events',
     'appropriate_grades_min', 'appropriate_grades_max', 'tags', 'sub_tags', 'question_maker', 'last_change_date']
            }
    readonly_fields_types = { 
        'a' : ['question_maker', 'last_change_date', 'events', 'verification_status'],
        's' : ['question_maker', 'last_change_date']
    }

    fields = fields_types['s']
    readonly_fields = readonly_fields_types['s']
    
    list_display = ('name', 'verification_status' , 'last_change_date', 'question_maker')
    list_filter = ['verification_status', 'question_maker']
    form = QuestionForm
    
    #all defualt saved for each users
    def save_model(self, request, obj, form, change):
        if not change:
            obj.question_maker = request.user.account
            #request.user.account.last_added_question
            #request.user.account.save()
            
        if obj.question_maker.role is 'a':
            obj.verification_status = 'w'
        
        obj.last_change_date = timezone.localtime()
        obj.save()
    
    def add_view(self, request, form_url='', extra_context=None):
        if request.user.account.role is 'a':
            self.fields = self.fields_types['a']
    
        return super().add_view(
            request, form_url, extra_context=extra_context,
        )
   
    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.account.role is 'a':
            self.readonly_fields = self.readonly_fields_types['a']
            self.fields = self.fields_types['s']
    
        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )
   

    #def get_form(self, request, obj=None, **kwargs):
        #form = super(QuestionAdmin, self).get_form(request, obj, **kwargs)
        #if(obj is None and request.user.account.last_added_question is not None):
            #form.base_fields['level'].initial = request.user.account.last_added_question.level
            #form.base_fields['source'].initial = request.user.account.last_added_question.source
            #form.base_fields['events'].initial = request.user.account.last_added_question.events
            #form.base_fields['appropriate_grades_min'].initial = request.user.account.last_added_question.appropriate_grades_min
            #form.base_fields['appropriate_grades_max'].initial = request.user.account.last_added_question.appropriate_grades_max
            #form.base_fields['tags'].initial = request.user.account.last_added_question.tags
            #form.base_fields['sub_tags'].initial = request.user.account.last_added_question.sub_tags
            
    #    return form
    
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
        return True if request.user.is_superuser or request.user.account.role is 'm' or  obj is None else request.user.account.question_set.filter(
            id=obj.id).exists()



class AccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'numberOfAdds', 'last_added_question')
    form = AccountForm
    fields = ['user', 'role', 'phone_number', 'email', 'scientific_rate', 'contribution_rate']

    def change_view(self, request, object_id, form_url='', extra_context=None):
        if request.user.account.role is 'a':
            self.fields = ['user', 'role', 'scientific_rate', 'contribution_rate']

        return super().change_view(
            request, object_id, form_url, extra_context=extra_context,
        )

    def has_view_permission(self, request, obj=None):
        return True
    
    def has_module_permission(self, request):
        return True


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