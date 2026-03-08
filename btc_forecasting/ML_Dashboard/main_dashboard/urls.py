from django.contrib import admin
from django.urls import path
from monitoring.views import dashboard_overview, drift_monitoring, prediction_ui
from experiments.views import experiment_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_overview, name='dashboard'),
    path('experiments/', experiment_list, name='experiments'),
    path('monitoring/drift/', drift_monitoring, name='drift'),
    path('prediction/', prediction_ui, name='prediction'),
]
