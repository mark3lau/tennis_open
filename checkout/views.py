from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag")
        return redirect(reverse('checkout'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51MyYnbBPaZVYK7rUSwxbvbS9lj3FSzjhdDE8WnchAn4rozZQoyU17gheBq6vizMYbSEqrtLMxOFOdmOf88i1F35S00KusiS5U6',
        'client_secret': 'test client secret',
    }
    return render(request, template, context)