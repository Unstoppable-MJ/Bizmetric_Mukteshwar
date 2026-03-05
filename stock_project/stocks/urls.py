from django.urls import path
from .views import (
    LoginAPIView,
    PortfolioListAPIView,
    AddStockAPIView,
    StockListAPIView,
    StockPreviewAPIView,
    MultiStockHistoryAPIView,
    PortfolioStockDetailAPIView,
    StockPredictionAPIView,
    StockClusteringAPIView,
    PortfolioGrowthAPIView, # Added PortfolioGrowthAPIView
    Nifty50PCAAPIView,
    PreciousMetalsAPIView,
    CryptoForecastingAPIView,
)

urlpatterns = [
    path('login/', LoginAPIView.as_view()),
    path('portfolios/', PortfolioListAPIView.as_view()),
    path('add-stock/', AddStockAPIView.as_view()),
    path('portfolio-stocks/', StockListAPIView.as_view()),
    path('portfolio-stocks/<int:pk>/', PortfolioStockDetailAPIView.as_view()),
    path('stock-preview/', StockPreviewAPIView.as_view()),
    path('portfolio-history/', MultiStockHistoryAPIView.as_view()),
    path('stock-prediction/', StockPredictionAPIView.as_view()),
    path('stock-clustering/', StockClusteringAPIView.as_view()),
    path('portfolio-growth/', PortfolioGrowthAPIView.as_view()), # Registered PortfolioGrowthAPIView
    path('nifty50-pca/', Nifty50PCAAPIView.as_view()),
    path('precious-metals/', PreciousMetalsAPIView.as_view()),
    path('crypto-ai/', CryptoForecastingAPIView.as_view()),
]