from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'store'

urlpatterns = [
    # root directory 
    path('', views.product_all, name = 'product_all'),
    path('<slug:slug>', views.product_detail, name = 'product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name = 'category_list'),
]