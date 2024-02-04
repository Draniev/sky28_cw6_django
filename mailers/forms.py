from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django import forms

from mailers.models import Subscriber, Distribution

User = get_user_model()

SubscriberFormSet = inlineformset_factory(User, Subscriber, fields=['email', 'first_name', 'last_name'], extra=1)


class DistributionForm(forms.ModelForm):
    class Meta:
        model = Distribution
        # fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
        self.fields['stop_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
        self.fields['mailing_time'].widget.attrs['class'] = 'form-control datetimepicker-input'
