from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages
from tennis_lessons.models import Package
from django.views.decorators.http import require_POST


def add_to_bag(request, package_id):
    """ Add a package to the shopping bag """

    package = Package.objects.get(pk=package_id)
    bag = request.session.get('bag', {})
    if package_id in bag:
        bag[package_id] += 1
    else:
        bag[package_id] = 1
        messages.success(request, f'Added {package.name} to your bag')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def view_bag(request):
    """ A view to render the bag contents page """

    return render(request, 'bag/bag.html')


def remove_from_bag(request, package_id):
    """ Remove an item from the bag """

    package = Package.objects.get(pk=package_id)
    bag = request.session.get('bag', {})
    
    if package_id in bag:
        bag.pop(package_id)
        messages.success(request, f'Removed {package.name} from your bag')

    request.session['bag'] = bag
    return HttpResponse(status=200)


