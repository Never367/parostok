from django.urls import path

from .views import MainView, CategoryListView, SubCategoryListView, ProductDetailView, SearchListView

urlpatterns = [
    path('search/', SearchListView.as_view(), name='search_results'),
    path('', MainView.as_view(), name='main'),
    path('<str:slug>/', CategoryListView.as_view(), name='category_detail'),
    path('<str:category_slug>/<str:slug>/', SubCategoryListView.as_view(),
         name='subcategory_detail'),
    path('<str:category_slug>/<str:subcategory_slug>/<str:slug>/',
         ProductDetailView.as_view(), name='product_detail'),
]
