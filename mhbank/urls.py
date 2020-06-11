from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views.questionview import *
from .views.accountview import *

urlpatterns = [
    path('question/', question_list.as_view()),
    path('question/<int:pk>/', question_detail),

    path('account/', account_list),
    path('account/<int:pk>/', account_detail),
    path('login/', obtain_auth_token),
]
