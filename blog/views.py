from random import sample

from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
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

    @method_decorator(cache_page(60 * 15))  # Кэширование страницы на 15 минут
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.views += 1
        self.object.save()
        return super().get(request, *args, **kwargs)


class HomePageView(View):
    template_name = 'blog/home_page.html'

    def get(self, request, *args, **kwargs):
        # Try to get parameters from the cache
        total_subscribers = cache.get('total_subscribers')
        total_mailings = cache.get('total_mailings')
        active_mailings = cache.get('active_mailings')

        # Calculate the required parameters if cashe is None
        if total_subscribers is None:
            total_subscribers = Subscriber.objects.values('email').distinct().count()
            cache.set('total_subscribers', total_subscribers)
        if total_mailings is None:
            total_mailings = Distribution.objects.count()
            cache.set('total_mailings', total_mailings)
        if active_mailings is None:
            active_mailings = Distribution.objects.filter(status=Distribution.Status.STARTED).count()
            cache.set('active_mailings', active_mailings)

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
