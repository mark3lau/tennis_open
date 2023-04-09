from django.shortcuts import render, get_object_or_404, redirect
from .models import Package
from django.contrib import messages


def all_packages(request):
    """ A view to show all tennis and fitness packages """

    packages = Package.objects.all()

    if request.method == 'POST':
        package_id = request.POST.get('package_id')
        if package_id:
            bag = request.session.get('bag', {})
            if package_id in bag:
                bag[package_id] += 1
            else:
                bag[package_id] = 1
            request.session['bag'] = bag
            package = get_object_or_404(Package, pk=package_id)
            messages.success(request, f'Added {package.name} to your bag')
            return redirect('all_packages')

    context = {
        'packages': packages,
    }

    return render(request, 'packages/packages.html', context)
