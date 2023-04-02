from django.shortcuts import render
from .models import Package


def tennis_fitness_packages(request):
    """ A view to show all tennis and fitness packages """

    packages = Package.objects.all()

    context = {
        'packages': packages,
    }
    
    return render(request, 'packages/packages.html', context)