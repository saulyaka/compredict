from django.urls import path
from .views import StandardDeviationView

urlpatterns = [
    path('', StandardDeviationView.as_view(), name='normalization'),
]
