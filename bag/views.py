from django.shortcuts import render, redirect, reverse

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

