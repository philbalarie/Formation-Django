from django.shortcuts import render
from travels.models import Travel, Destination

def travels(request):
    travels = Travel.objects.all()

    context = {
        'travels' : travels
    }

    return render(request, 'travels/travels.html', context)

def travel(request, slug):

    travel = Travel.objects.get(slug=slug)

    context = { 'travel' : travel }

    return render(request, 'travels/travel.html', context)