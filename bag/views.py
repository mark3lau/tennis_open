from django.shortcuts import render, redirect


def view_bag(request):
    """ A view to render the bag contents page """
    
    return render(request, 'bag/bag.html')


def add_to_bag(request, item_id):
    """Add a package to the bag """

    redirect_url = request.POST.get('redirect_url')
    bag = request.session.get('bag', {})\
    
    request.session['bag'] = bag
    print(request.session['bag'])
    return redirect(redirect_url)
