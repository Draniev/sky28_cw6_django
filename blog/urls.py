from django.urls import path

from blog.views import BlogPostListView, BlogPostDetailView, HomePageView

app_name = 'blog'

urlpatterns = [
    path('', HomePageView.as_view(), name='index'),
    path('blog/', BlogPostListView.as_view(), name='list'),
    path('blog/<int:pk>/', BlogPostDetailView.as_view(), name='detail'),
]