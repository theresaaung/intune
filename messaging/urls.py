from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:username>/', views.conversation, name='conversation'),
    path('notifications/', views.notifications, name='notifications'),
]