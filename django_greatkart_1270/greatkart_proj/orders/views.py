from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from cart.models import Cart, CartItem
from orders.models import Order
from store.models import Product

from django.contrib import messages
@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart.html', {'cart': cart})

@login_required
def checkout(request):
    # Get the user's cart
    cart, created = Cart.objects.get_or_create(user=request.user)

    
    cart_items = CartItem.objects.filter(cart=cart)

    # If cart is empty, do not allow checkout
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty. Please add items before checking out.")
        return redirect('view_cart')  # Replace 'cart' with your cart view name

    # Calculate the total price, tax, and grand total
    total_price = sum([item.quantity * item.product.price for item in cart_items])
    tax = total_price * 0.10  
    grand_total = total_price + tax

    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        country = request.POST.get('country')
        state = request.POST.get('state')
        address = request.POST.get('address')
        building = request.POST.get('building')
        house = request.POST.get('house')
        postal_code = request.POST.get('postal_code')
        zip_code = request.POST.get('zip')
        payment_option = request.POST.get('payment_option')
        total = request.POST.get('total')

        
        order = Order.objects.create(
            user=request.user,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            country=country,
            state=state,
            address=address,
            building=building,
            house=house,
            postal_code=postal_code,
            zip_code=zip_code,
            total_price=total_price,
            tax=tax,
            grand_total=grand_total,
            payment_option=payment_option,
            status="Pending"
        )

        
        for item in cart_items:
            order.order_items.create(
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        
        cart_items.delete()

        
        

        
        return redirect('order_success', order_id=order.id)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'place-order.html', context)



def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    context = {
        'order': order
    }
    return render(request, 'order_detail.html', context)
