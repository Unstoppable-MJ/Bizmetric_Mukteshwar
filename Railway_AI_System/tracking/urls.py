from django.urls import path
from .views import GetTrainStatusView, GetTrainPredictionView

urlpatterns = [
    path('train/<str:train_no>/', GetTrainStatusView.as_view(), name='get_train_status'),
    path('predict/<str:train_no>/', GetTrainPredictionView.as_view(), name='get_train_prediction'),
]
