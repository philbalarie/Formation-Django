from django.shortcuts import render

def travels(request):
    return render(request, 'travels/travels.html')
