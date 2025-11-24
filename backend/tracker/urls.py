from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'register', views.UserRegistrationViewSet, basename='register')
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'expenses', views.ExpenseViewSet, basename='expense')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', views.UserProfileView.as_view(), name='user-profile'),

    path('auth/password_reset/', views.RequestPasswordResetEmail.as_view(), name='password-reset-request'),
    path('auth/reset/<str:uidb64>/<str:token>/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
]
