from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name="register"),
    path('<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('<int:pk>/edit/', views.UserUpdate.as_view(), name='user_edit'),
    path('list/', views.UsersListView.as_view(), name='users_list'),
    path('<int:pk>/style/', views.ColorChangeView.as_view(), name='style_edit'),

]
