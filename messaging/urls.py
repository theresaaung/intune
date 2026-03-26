from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('conversation/<str:username>/', views.conversation, name='conversation'),
    path('notifications/', views.notifications, name='notifications'),
    path('send/<int:match_id>/', views.send_message, name='send_message'),
    path('mark-all-read/', views.mark_all_read, name='mark_all_read'),
]