from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.utils import timezone

from mhbank.models import Question, Account, Answer, Guidance
import datetime

JUST_VIEW_METHODS = ['GET']
JUST_ADD_METHODS = ['POST', 'GET']
EDIT_AND_DELET_METHODS = ['POST', 'GET', 'PUT', 'DELET']
SAFE_METHODS = ['POST', 'GET', 'PUT', 'DELET']
"""
POST = ADD NEW ONE
PUT = CHANGE
GET = READ
DELET = DELET
"""
class DefualtPermission(BasePermission):
    def has_anonymous_permission(self, request, view):
        return False 
        
    def has_adder_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS    
    
    def has_mentor_permission(self, request, view):
        return request.method in JUST_ADD_METHODS

    def has_permission(self, request, view):
        if request.user.is_anonymous :
            return self.has_anonymous_permission(request, view)
        elif request.user.account.is_adder() :
            return self.has_adder_permission(request, view)
        elif request.user.account.is_mentor() :
            return self.has_mentor_permission(request, view)
        elif request.user.account.is_superuser() :
            return request.method in SAFE_METHODS
        else :
            return False

class CommentPermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return request.method in JUST_ADD_METHODS

    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS

class QuestionPermission(DefualtPermission):

    def is_my_object(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            question = Question.objects.get(pk=pk)
        except:
            return False
        
        return request.user.account.id == question.question_maker.id
 
    def is_waiting(self, request, view):
        return False
        ###
        try:
            pk = request.parser_context['kwargs']['pk']
            question = Question.objects.get(pk=pk)
        except:
            return False
 
        return question.verification_status == 'w' or question.verification_status == 'r'
        
    def is_not_list(self, request):
        try:
            request.parser_context['kwargs']['pk']
            return request.method in ['GET']
        except: 
            pass
        return False

    def has_anonymous_permission(self, request, view):
        return (request.method in ['GET']) and not self.is_waiting(request, view) and self.is_not_list(request)

    def has_adder_permission(self, request, view):
        return ( (request.method in ['POST']) or \
            ((request.method in ['GET']) and  ( self.is_my_object(request, view) or not self.is_waiting(request, view)) ) or \
            (request.method in EDIT_AND_DELET_METHODS and self.is_my_object(request, view)) ) \
            #and self.is_not_list(request)

    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS

class AnswerPermission(DefualtPermission):

    def is_my_object(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            answer = Answer.objects.get(pk=pk)
        except:
            return False
        
        return  (request.user.account.id == answer.question.question_maker.id) or \
                (request.user.account.id == answer.account.id)

    def has_anonymous_permission(self, request, view):
        return request.method in JUST_ADD_METHODS
        
    def has_adder_permission(self, request, view):
        return  request.method in ['POST'] or \
                (request.method in EDIT_AND_DELET_METHODS and self.is_my_object(request, view))

    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS

class GuidancePermission(DefualtPermission):

    def has_adder_permission(self, request, view):
        return  request.method in ['POST']
        
    def has_mentor_permission(self, request, view):
        return request.method in SAFE_METHODS


class AccountPermission(DefualtPermission):

    def is_my_account(self, request, view):
        try:
            pk = request.parser_context['kwargs']['pk']
            account = Account.objects.get(pk=pk)
        except:
            return True
        
        return request.user.account.id == account.id

    def has_adder_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS
    
    def has_mentor_permission(self, request, view):
        return request.method in JUST_VIEW_METHODS

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
    
