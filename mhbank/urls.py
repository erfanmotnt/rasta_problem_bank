from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from .views.questionview import *
from .views.accountview import *
from .views.registerView import *

router = DefaultRouter()
router.register('account', AccountView)

urlpatterns = [
    path('question/', question_list.as_view()),
    path('question/<int:pk>/', question_detail),

    path('signup/', register),
    path('signin/', obtain_auth_token),
]

urlpatterns += router.urls
