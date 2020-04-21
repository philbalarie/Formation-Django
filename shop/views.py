from django.shortcuts import render, redirect, get_object_or_404
from travels.models import Travel, OrderTravel, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import stripe
import simplejson
import time

@login_required
def cart(request):

    if request.method == 'POST':
        # Récupère les données du formulaire
        quantity = request.POST.get('quantity')
        travel_slug = request.POST.get('travel_slug')

        # Récupère l'objet travel dans la BDD grâce aux infos du formulaire
        travel = get_object_or_404(Travel, slug=travel_slug)
        
        # Vérifie si une queryset existe avec les conditions du formulaire
        orderTravel_qs = OrderTravel.objects.filter(travel=travel, user=request.user, ordered=False)

        # Si l'utilisateur a déjà commandé le voyage, on augmente la quantité
        if orderTravel_qs:
            orderTravel = orderTravel_qs[0]
            orderTravel.quantity += int(quantity)
            orderTravel.save()
        else: # Sinon, on crée le orderTravel
            orderTravel = OrderTravel.objects.create(quantity=quantity, travel=travel, user=request.user)

        # Gestion de la commande
        order_qs = Order.objects.filter(user=request.user, ordered=False)

        if order_qs:
            order = order_qs[0]
            order.travels.add(orderTravel)
        else:
            order = Order.objects.create(user=request.user)
            order.travels.add(orderTravel)

    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs:
        order = order_qs[0]

        context = { 'order' : order }

        return render(request, 'shop/shopping_cart.html', context)
    
    else:
        return render(request, 'shop/shopping_cart.html')

    return render(request, 'shop/shopping_cart.html')

@login_required
def checkout(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        order = Order.objects.get(user=request.user, ordered=False)

        line_items = []

        for order_travel in order.travels.all():
            line_items.append({
                'name' : order_travel.travel.destination.hotel_name,
                'description': order_travel.travel.destination.description,
                'amount' : int(order_travel.travel.price) * 100,
                'currency' : 'cad',
                'quantity' : int(order_travel.quantity)

                })

        stripe_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        customer_email=request.user.email,
        line_items=line_items,
        success_url='http://127.0.0.1:8000/accounts/dashboard?p=success',
        cancel_url='http://127.0.0.1:8000/accounts/dashboard?p=failure',
    )
        #TODO: Ajouter la gestion des erreurs et la gestion de la page de confirmation
        simplejson.dumps(stripe_session['id'])

        stripe_id = simplejson.dumps(stripe_session['id'])

        return render(request, 'shop/checkout.html', {'stripe_id' : stripe_id})
        

    except ObjectDoesNotExist:
        messages.info('Vous n\'avez présentement aucun voyage dans votre panier')
        return redirect('cart')

@csrf_exempt
def payment_completed_hook(request):
    #FIXME: Valider la gestion du webhooks qui renvoit des 404...

    endpoint_secret = 'whsec_...'

    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, 
        sig_header, 
        endpoint_secret
            )

    except ValueError as e:
        print('ca ne fonctione pas...')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print('Ca ne fonctionne toujours pas...')
        return HttpResponse(status=400)

            # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        #FIXME: Fixer le fait que ces comportements ne veulent pas arriver


        def handle_checkout_session(session):
            order_qs = Order.objects.all()

            if order_qs.exists():
                order = order_qs[0]

                order.ordered = True
                for orderTravel in order.travels.all():
                    orderTravel.ordered = True
                    orderTravel.save()
                order.save()

        handle_checkout_session(session)

        return HttpResponse(status=200)

@login_required
def add_travel_to_cart(request, slug):

    order_qs = Order.objects.get(user=request.user, ordered=False)

    travelOrder_qs = OrderTravel.objects.filter(travel__slug=slug)

    if travelOrder_qs.exists():
        travelOrder = travelOrder_qs[0]
        travelOrder.quantity += 1
        travelOrder.save()

    return redirect('cart')

@login_required
def remove_travel_to_cart(request, slug):

    order_qs = Order.objects.filter(user=request.user, ordered=False)
    
    travelOrder_qs = OrderTravel.objects.filter(travel__slug=slug)

    if travelOrder_qs.exists():
        travelOrder = travelOrder_qs[0]
        travelOrder.quantity -= 1
        travelOrder.save()

        if travelOrder.quantity == 0:
            travelOrder.delete()

            if order_qs[0].travels.count() == 0:
                order_qs[0].delete()

    return redirect('cart')
