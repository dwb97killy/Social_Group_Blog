from django.urls import path
from accounts import views
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('<int:pk>/', views.user_profile_login, name='user_profile_login'),
    path('visitor/<int:pk>/', views.user_profile_customer, name='user_profile_customer'),
    path('blog/draft_blog', views.DraftBlog.as_view(), name='draft_blog'),
]
