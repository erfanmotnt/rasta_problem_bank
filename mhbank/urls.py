from django.urls import path
from mhbank import views

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/', views.question_list),
    path('question/<int:pk>/', views.question_detail),

    path('account/', views.account_list),
    path('account/<int:pk>/', views.account_detail),
]
