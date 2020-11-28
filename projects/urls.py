from django.conf.urls import url

from .views import ProjectHomeView, CreateProjectView, TakenProjectsView, EditProjectView, DeleteProjectView
from django.urls import path


urlpatterns = [
    path('', ProjectHomeView.as_view(), name='project_home'),
    path('create/', CreateProjectView.as_view(), name='create_project'),
    path('view/', TakenProjectsView.as_view() , name='view_all_projects'),
    path('edit/<int:project_id>', EditProjectView.as_view(), name='edit_project'),
    path('delete/<int:project_id>', DeleteProjectView.as_view(), name='delete_project')

]