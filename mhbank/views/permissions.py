from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

from mhbank.models import Question

NOCHANGE_METHODS = ['POST', 'GET']
NODELET_METHODS = ['POST', 'GET', 'PUT']
#SAFE_METHODS = ['POST', 'GET', 'PUT', 'DELET']

class DefualtPermission(BasePermission):

    def has_adder_permission(self, request, view):
        return request.method in NOCHANGE_METHODS    
    
    def has_mentor_permission(self, request, view):
        return request.method in NODELET_METHODS
      
    def has_permission(self, request, view):
        if  (self.has_adder_permission(request, view) and request.user.account.is_adder()) or \
            (self.has_mentor_permission(request, view) and request.user.account.is_mentor()) or \
            (request.method in SAFE_METHODS and request.user.account.is_superuser()):
            return True
        return False

class QuestionPermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            question = Question.objects.get(pk=pk)
        except:
            return (request.method in SAFE_METHODS)


        return  (request.method in NOCHANGE_METHODS) or \
                (request.method in SAFE_METHODS and question.question_maker is request.user.account)

    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS

class AccountPermission(DefualtPermission):

    def has_mentor_permission(self, request, view):
        return request.method in NOCHANGE_METHODS

class TagPermission(DefualtPermission):
 
    def has_mentor_permission(self, request, view):
        return request.method in NOCHANGE_METHODS

class SubTagPermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return request.method in NODELET_METHODS

class EventPermission(DefualtPermission):
    pass

class SourcePermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return request.method in NODELET_METHODS
    
