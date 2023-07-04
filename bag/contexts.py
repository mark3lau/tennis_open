from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from tennis_lessons.models import Package


def bag_contents(request):

    bag_items = []
    total = 0
    bag = request.session.get('bag', {})

    for package_id, quantity in bag.items():
        package = get_object_or_404(Package, pk=package_id)
        total += package.price
        bag_items.append({
            'package_id': package_id,
            'quantity': quantity,
            'name': package.name,
            'description': package.description,
            'price': package.price,
        })

    context = {
        'bag_items': bag_items,
        'total': total,
    }

    return context