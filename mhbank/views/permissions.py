from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.utils import timezone

from mhbank.models import Question, Account
import datetime

JUST_VIEW_METHODS = ['GET']
JUST_ADD_METHODS = ['POST', 'GET']
EDIT_AND_DELET_METHODS = ['POST', 'GET', 'PUT', 'DELET']
#SAFE_METHODS = ['POST', 'GET', 'PUT', 'DELET']
"""
POST = ADD NEW ONE
PUT = CHANGE
GET = READ
DELET = DELET
"""
class DefualtPermission(BasePermission):
        
    def has_adder_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS    
    
    def has_mentor_permission(self, request, view):
        return  request.method in JUST_ADD_METHODS

    def has_permission(self, request, view):
        if  (self.has_adder_permission(request, view) and request.user.account.is_adder()) or \
            (self.has_mentor_permission(request, view) and request.user.account.is_mentor()) or \
            (request.method in SAFE_METHODS and request.user.account.is_superuser()):
            return True
        return False

class QuestionPermission(DefualtPermission):

    def is_my_object(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            question = Question.objects.get(pk=pk)
        except:
            return False
        
        return self.request.user.account.id == question.question_maker.id

    def has_adder_permission(self, request, view):
        return  request.method in JUST_ADD_METHODS or \
                (request.method in EDIT_AND_DELET_METHODS and self.is_my_object())

    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS

class AccountPermission(DefualtPermission):

    def is_my_account(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            account = Account.objects.get(pk=pk)
        except:
            return True
        
        return self.request.user.account.id == account.id

    def has_mentor_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS and self.is_my_account()

class TagPermission(DefualtPermission):
 
    def has_mentor_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS

class SubTagPermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return request.method in JUST_ADD_METHODS

class EventPermission(DefualtPermission):
    pass

class SourcePermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return request.method in JUST_ADD_METHODS
    
