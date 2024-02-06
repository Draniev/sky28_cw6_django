from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, ListView

from mailers.forms import DistributionForm, MailingListForm
from mailers.models import Subscriber, MailingList, Message, Distribution, DistributionLog


def test_mail_view(request):
    send_mail('Тестовое письмо',
              'Тело письма',
              'info@bid-trade.ru',
              ['sergan.mail@gmail.com'])

    return render(request, 'mailers/test_mail.html')


def new_app(request):
    return render(request, 'mailers/app.html')


class OwnerRequiredMixin(UserPassesTestMixin):
    """
    Mixin to check if the request user is the owner of the object
    and the request user has a confirmed e-mail address
    """
    raise_exception = True

    def test_func(self):
        obj = self.get_object()
        user = self.request.user
        return user == obj.owner and user.is_email_verified


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = 'mailers/subscribers.html'
    context_object_name = 'subscribers'
    login_url = reverse_lazy('users:sign-in')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    template_name = 'mailers/subscriber_form.html'
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('mailers:subscribers')
    login_url = reverse_lazy('users:sign-in')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class SubscriberUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Subscriber
    template_name = 'mailers/subscriber_form.html'
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('mailers:subscribers')
    login_url = reverse_lazy('users:sign-in')


class SubscriberDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Subscriber
    template_name = 'mailers/subscriber_confirm_delete.html'
    success_url = reverse_lazy('mailers:subscribers')
    login_url = reverse_lazy('users:sign-in')


class MailingListListView(LoginRequiredMixin, ListView):
    model = MailingList
    template_name = 'mailers/mailinglist_list.html'
    context_object_name = 'mailing_lists'
    login_url = reverse_lazy('users:sign-in')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class MailingListCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mailers/mailinglist_form.html'
    # fields = ['name', 'subscribers']
    success_url = reverse_lazy('mailers:mailing_lists')
    login_url = reverse_lazy('users:sign-in')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class MailingListUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = MailingList
    form_class = MailingListForm
    template_name = 'mailers/mailinglist_form.html'
    # fields = ['name', 'subscribers']
    success_url = reverse_lazy('mailers:mailing_lists')
    login_url = reverse_lazy('users:sign-in')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class MailingListDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = MailingList
    template_name = 'mailers/mailinglist_confirm_delete.html'
    success_url = reverse_lazy('mailers:mailing_lists')
    login_url = reverse_lazy('users:sign-in')


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'mailers/message_list.html'
    context_object_name = 'messages'
    login_url = reverse_lazy('users:sign-in')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = 'mailers/message_form.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('mailers:messages')
    login_url = reverse_lazy('users:sign-in')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class MessageUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Message
    template_name = 'mailers/message_form.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('mailers:messages')
    login_url = reverse_lazy('users:sign-in')


class MessageDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Message
    template_name = 'mailers/message_confirm_delete.html'
    success_url = reverse_lazy('mailers:messages')
    login_url = reverse_lazy('users:sign-in')


class DistributionListView(LoginRequiredMixin, ListView):
    model = Distribution
    template_name = 'mailers/distribution_list.html'
    context_object_name = 'distributions'
    login_url = reverse_lazy('users:sign-in')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class DistributionCreateView(LoginRequiredMixin, CreateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'mailers/distribution_create.html'
    success_url = reverse_lazy('mailers:distribution_list')
    login_url = reverse_lazy('users:sign-in')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class DistributionUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'mailers/distribution_edit.html'
    success_url = reverse_lazy('mailers:distribution_list')
    login_url = reverse_lazy('users:sign-in')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class DistributionDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = Distribution
    template_name = 'mailers/distribution_confirm_delete.html'
    success_url = reverse_lazy('mailers:distribution_list')
    login_url = reverse_lazy('users:sign-in')


class DistributionLogListView(LoginRequiredMixin, ListView):
    model = DistributionLog
    template_name = 'mailers/distributionlog_list.html'
    context_object_name = 'distributionslog'
    login_url = reverse_lazy('users:sign-in')

    def get_queryset(self):
        return self.model.objects.filter(owner=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)
