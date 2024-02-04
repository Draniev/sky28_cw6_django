from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, DeleteView, CreateView, ListView

from mailers.forms import DistributionForm
from mailers.models import Subscriber, MailingList, Message, Distribution, DistributionLog


def test_mail_view(request):
    send_mail('Тестовое письмо',
              'Тело письма',
              'info@bid-trade.ru',
              ['sergan.mail@gmail.com'])

    return render(request, 'mailers/test_mail.html')


def new_app(request):
    return render(request, 'mailers/app.html')


class SubscriberListView(LoginRequiredMixin, ListView):
    model = Subscriber
    template_name = 'mailers/subscribers.html'
    context_object_name = 'subscribers'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_email_verified:
            return redirect(reverse_lazy('users:activate'))
        return super().dispatch(request, *args, **kwargs)


class SubscriberCreateView(LoginRequiredMixin, CreateView):
    model = Subscriber
    template_name = 'mailers/subscriber_form.html'
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('mailers:subscribers')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class SubscriberUpdateView(LoginRequiredMixin, UpdateView):
    model = Subscriber
    template_name = 'mailers/subscriber_form.html'
    fields = ['email', 'first_name', 'last_name']
    success_url = reverse_lazy('mailers:subscribers')


class SubscriberDeleteView(LoginRequiredMixin, DeleteView):
    model = Subscriber
    template_name = 'mailers/subscriber_confirm_delete.html'
    success_url = reverse_lazy('mailers:subscribers')


class MailingListListView(LoginRequiredMixin, ListView):
    model = MailingList
    template_name = 'mailers/mailinglist_list.html'
    context_object_name = 'mailing_lists'


class MailingListCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    template_name = 'mailers/mailinglist_form.html'
    fields = ['name', 'subscribers']
    success_url = reverse_lazy('mailers:mailing_lists')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MailingListUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingList
    template_name = 'mailers/mailinglist_form.html'
    fields = ['name', 'subscribers']
    success_url = reverse_lazy('mailers:mailing_lists')


class MailingListDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingList
    template_name = 'mailers/mailinglist_confirm_delete.html'
    success_url = reverse_lazy('mailers:mailing_lists')


class MessageListView(ListView):
    model = Message
    template_name = 'mailers/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailers/message_form.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('mailers:messages')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailers/message_form.html'
    fields = ['title', 'body']
    success_url = reverse_lazy('mailers:messages')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailers/message_confirm_delete.html'
    success_url = reverse_lazy('mailers:messages')


class DistributionListView(ListView):
    model = Distribution
    template_name = 'mailers/distribution_list.html'
    context_object_name = 'distributions'


class DistributionCreateView(CreateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'mailers/distribution_create.html'
    success_url = reverse_lazy('mailers:distribution_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class DistributionUpdateView(UpdateView):
    model = Distribution
    form_class = DistributionForm
    template_name = 'mailers/distribution_edit.html'
    success_url = reverse_lazy('mailers:distribution_list')


class DistributionDeleteView(DeleteView):
    model = Distribution
    template_name = 'mailers/distribution_confirm_delete.html'
    success_url = reverse_lazy('mailers:distribution_list')


class DistributionLogListView(ListView):
    model = DistributionLog
    template_name = 'mailers/distributionlog_list.html'
    context_object_name = 'distributionslog'
