from django.urls import path
from .views import ErrorView

urlpatterns = [
    path('', ErrorView.as_view(), name='error')
]
