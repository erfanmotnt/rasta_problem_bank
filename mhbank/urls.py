from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views.questionview import *
from .views.accountview import *
from .views.registerView import *
from .views.tagview import *
from .views.subtagview import *
from .views.eventview import *
from .views.sourceview import *

router = DefaultRouter()
router.register('account', AccountView)
router.register('question', QuestionView)
router.register('tag', TagView)
router.register('subtag', SubTagView)
router.register('event', EventView)
router.register('source', SourceView)

urlpatterns = [
    path('signup/', register),
    path('signin/', obtain_auth_token),
]

urlpatterns += router.urls
