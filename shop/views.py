from django.shortcuts import render, redirect, get_object_or_404
from travels.models import Travel, OrderTravel, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import stripe
import simplejson

def cart(request):

    if request.user.is_authenticated:

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
            
    else:
        return redirect('login')
        

    return render(request, 'shop/shopping_cart.html')

def checkout(request):

    stripe.api_key = 'sk_test_xrwfhsOIbGwnMyvv3C0qHc7600pS7pF05p'

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



def add_travel_to_cart(request, slug):

    order_qs = Order.objects.get(user=request.user, ordered=False)

    travelOrder_qs = OrderTravel.objects.filter(travel__slug=slug)

    if travelOrder_qs.exists():
        travelOrder = travelOrder_qs[0]
        travelOrder.quantity += 1
        travelOrder.save()

    return redirect('cart')

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
