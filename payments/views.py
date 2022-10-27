from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse
from awards.models import Award

import stripe

class HomePageView(TemplateView):
    template_name = 'payments/home.html'

class SuccessView(TemplateView):
    template_name = 'payments/success.html'

class CancelledView(TemplateView):
    template_name = 'payments/cancelled.html'

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@login_required(login_url='/login/')
@csrf_exempt
def create_checkout_session(request, tier, price_id):
    if request.method == 'GET':
        domain_url = 'http://%s/' % (request.get_host())
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                metadata={'tier': tier},
                client_reference_id=request.user.id,
                payment_method_types=['card'],
                line_items=[{
                    'price': price_id,
                    'quantity': 1,
                }],  
                mode='payment',
                success_url=domain_url + reverse('success') + '?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + reverse('cancelled'),
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        user = User.objects.get(id=event.data.object.client_reference_id)
        tier = event.data.object.metadata.tier
        Award.buy(user, tier)
        
    return HttpResponse(status=200)