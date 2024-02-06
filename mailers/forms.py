from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django import forms

from mailers.models import Subscriber, Distribution, MailingList

User = get_user_model()

SubscriberFormSet = inlineformset_factory(User, Subscriber, fields=['email', 'first_name', 'last_name'], extra=1)


class MailingListForm(forms.ModelForm):
    class Meta:
        model = MailingList
        fields = ['name', 'subscribers']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['subscribers'].queryset = self.fields['subscribers'].queryset.filter(owner=user)


class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        # fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
        self.fields['stop_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
        self.fields['mailing_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
        if user:
            self.fields['mailing_list'].queryset = self.fields['mailing_list'].queryset.filter(owner=user)
            self.fields['message'].queryset = self.fields['message'].queryset.filter(owner=user)

