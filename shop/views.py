from django.shortcuts import render, redirect, get_object_or_404
from travels.models import Travel, OrderTravel, Order
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages

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

    try:
        order_qs = Order.objects.get(user=request.user, ordered=False)

        # FIXME: Ajouter le manager pour toutes les querysets pour chercher le order

        context = { 'order' : order_qs }

        return render(request, 'shop/checkout.html', context)

    except ObjectDoesNotExist:
        messages.info(request, 'Vous n\'avez présentement aucun voyage dans le panier')
        return redirect('index')

    return render(request, 'shop/checkout.html')

def add_travel_to_cart(request, slug):

    order_qs = Order.objects.get_user_order(request.user)

    return redirect('cart')
