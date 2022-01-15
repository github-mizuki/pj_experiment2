from django.urls import path
from .views import (
    HomeView, LogListView, MainTaskCreateView, MainTaskDetailView, LogUpdateView, MaintaskListView,
    MainTaskUpdateView, SubtaskListView, SubTaskCreateView, SubTaskUpdateView, ArchiveListView, archive_view
)


app_name = 'task'

urlpatterns = [
    path('task_home/', HomeView.as_view(), name='task_home'),
    path('log_list/', LogListView.as_view(), name='log_list'),
    path('maintask_create/', MainTaskCreateView.as_view(), name='maintask_create'),
    path('maintask_detail/<int:pk>', MainTaskDetailView.as_view(), name='maintask_detail'),
    path('maintask_update/<int:pk>', MainTaskUpdateView.as_view(), name='maintask_update'),
    path('subtask_create/<int:pk>', SubTaskCreateView.as_view(), name='subtask_create'),
    path('subtask_update/<int:pk>', SubTaskUpdateView.as_view(), name='subtask_update'),
    path('log_update/<int:pk>', LogUpdateView.as_view(), name='log_update'),
    path('archive_list/', ArchiveListView.as_view(), name='archive_list'),
    path('archive_view/<int:pk>', archive_view, name='archive_view'),
    path('maintask_list/', MaintaskListView.as_view(), name='maintask_list'),
    path('subtask_list/', SubtaskListView.as_view(), name='subtask_list'),
]