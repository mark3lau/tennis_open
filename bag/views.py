from django.shortcuts import render, redirect, reverse
from tennis_lessons.models import Package
from django.views.decorators.http import require_POST


def add_to_bag(request, package_id):
    """ Add a package to the shopping bag """

    bag = request.session.get('bag', {})
    if package_id in bag:
        bag[package_id] += 1
    else:
        bag[package_id] = 1
    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def view_bag(request):
    """ A view to render the bag contents page """

    return render(request, 'bag/bag.html')


@require_POST
def delete_from_bag(request, package_id):

    # Get the package object
    package = get_object_or_404(Package, pk=package_id)
    
    # Get the bag from the session
    bag = request.session.get('bag', {})
    
    # If the package is in the bag, remove it
    if package_id in bag:
        del bag[package_id]
        
    # Update the bag in the session
    request.session['bag'] = bag
    
    return redirect('view_bag')