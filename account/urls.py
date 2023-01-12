from django.contrib.auth import views as auth_views
from django.urls import path

from .views import LoginViewBase, LogoutViewBase, PasswordChangeViewBase, \
    PasswordResetViewBase, PasswordResetConfirmViewBase, register, edit, \
    orders, RegisterConfirmView, wish_list, wish_list_add, wish_list_remove

urlpatterns = [
    path('login/', LoginViewBase.as_view(), name='login'),
    path('logout/', LogoutViewBase.as_view(), name='logout'),
    path('password-change/', PasswordChangeViewBase.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password-reset/', PasswordResetViewBase.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', PasswordResetConfirmViewBase.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', register, name='register'),
    path('register/<uidb64>/<token>/', RegisterConfirmView.as_view(), name='register_confirm'),
    path('edit/', edit, name='edit'),
    path('orders/', orders, name='orders'),
    path('wish_list/', wish_list, name='wish_list'),
    path('wish_list/add/<str:product_id>/', wish_list_add, name='wish_list_add'),
    path('wish_list/remove/<str:product_id>/', wish_list_remove, name='wish_list_remove'),
]
