from django.urls import path
from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.BlogList.as_view(), name="all"),
    path("new/", views.CreateBlog.as_view(), name="create_blog"),
    # path("new/", views.CreateBlog, name="create_blog"),
    path("by/<username>/", views.UserBlog.as_view(), name="for_user"),
    path("by/<username>/<int:pk>/", views.BlogDetail.as_view(), name="blog_detail"),
    path("blog/create_success", views.CreateBlogSuccess.as_view(), name="blog_create_success"),
    path('by/<username>/<int:pk>/update', views.UpdateBlog.as_view(), name='update_blog'),
    path('by/<username>/<int:pk>/delete', views.DeleteBlog.as_view(), name='delete_blog'),
    path('by/<username>/<int:pk>/approve_comment', views.approve_comment, name='approve_comment'),
    path('by/<username>/<int:pk>/notapprove_comment', views.notapprove_comment, name='notapprove_comment'),
    path('by/<username>/<int:pk>/comment', views.add_comment, name='add_comment'),
    path('by/<username>/<int:pk>/publish', views.publish_blog, name='publish_blog'),
    path('by/<username>/<int:pk>/delete_comment', views.delete_comment, name='delete_comment'),
]