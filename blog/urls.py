from django.urls import path
from . import views
from blog.views import ChangePasswordView



urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('category/<str:slug>/', views.CategoryView, name='post_by_category'),
    path('post/<str:slug>/edit/', views.post_edit, name='post_edit'),
    path("signup/", views.signup, name="signup"),
    path("loginuser/", views.login_view, name="loginuser"),
    path("logout/", views.logout_view, name="logout"),
    path('profile/', views.profile_view, name='profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path("tags/<str:slug>/", views.list_posts_by_tag, name="tag"),


]