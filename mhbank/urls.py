from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views.questionview import *
from .views.accountview import *

urlpatterns = [
    path('question/', question_list.as_view()),
    path('question/<int:pk>/', question_detail),

    path('account/', AccountView.as_view()),
    path('login/', obtain_auth_token),
]
