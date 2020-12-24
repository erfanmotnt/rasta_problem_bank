from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views.commentview import *
from .views.questionview import *
from .views.accountview import *
from .views.registerView import *
from .views.tagview import *
from .views.subtagview import *
from .views.eventview import *
from .views.sourceview import *
from .views.filter import question_filter

router = DefaultRouter()
router.register('comment', CommentView)
router.register('comment/<int:pk>', CommentView)
router.register('account', AccountView)
router.register('account/<int:pk>', AccountView)
router.register('question', QuestionView)
router.register('question/<int:pk>', QuestionView)
router.register('tag', TagView)
router.register('tag/<int:pk>', TagView)
router.register('subtag', SubTagView)
router.register('subtag/<int:pk>', SubTagView)
router.register('event', EventView)
router.register('event/<int:pk>', EventView)
router.register('source', SourceView)
router.register('source/<int:pk>', SourceView)
# router.register('questionproperties', QuestionPropertiesView)
# router.register('questionproperties/<int:pk>', QuestionPropertiesView)

urlpatterns = [
    path('signup/', register),
    path('signin/', obtain_auth_token),
    path('signout/', signout),
    path('qfilter/', question_filter),
    path('accountbyusername/', account_by_username),
    
]

urlpatterns += router.urls
