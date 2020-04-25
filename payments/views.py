from django.views.generic.base import TemplateView
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

import stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


class confirmation(TemplateView):
    template_name = 'confirmation.html'

    @login_required
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


@login_required
def thanks(request):
    context = {}
    return render(request, 'payments/thanks.html', context)
