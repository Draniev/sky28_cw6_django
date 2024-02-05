from random import sample

from django.shortcuts import render
from django.views import View
from django.views.generic import ListView, DetailView

from blog.models import BlogPost
from mailers.models import Subscriber, Distribution


class BlogPostListView(ListView):
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'blogposts'
    ordering = ['-pub_date']
    paginate_by = 12


class BlogPostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'blogpost'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class HomePageView(View):
    template_name = 'blog/home_page.html'

    def get(self, request, *args, **kwargs):
        # Calculate the required parameters
        total_subscribers = Subscriber.objects.values('email').distinct().count()
        total_mailings = Distribution.objects.count()
        active_mailings = Distribution.objects.filter(status=Distribution.Status.STARTED).count()

        # Fetch three random articles from the blog
        all_blogposts = BlogPost.objects.all()
        random_blogposts = sample(list(all_blogposts), min(3, len(all_blogposts)))

        context = {
            'total_subscribers': total_subscribers,
            'total_mailings': total_mailings,
            'active_mailings': active_mailings,
            'blogposts': random_blogposts,
        }

        return render(request, self.template_name, context)
