from django.shortcuts import render, get_object_or_404
from .models import Package


def all_packages(request):
    """ A view to show all tennis and fitness packages """

    packages = Package.objects.all()

    context = {
        'packages': packages,
    }

    print(len(packages))
    
    return render(request, 'packages/packages.html', context)


def package_detail(request, package_id):
    """ A view to show details of all packages """

    package = get_object_or_404(Package, pk=package_id)

    context = {
        'package': package,
    }

    print(context)
    
    return render(request, 'packages/package_detail.html', context)