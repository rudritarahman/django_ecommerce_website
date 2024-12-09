import logging
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from sslcommerz_lib import SSLCOMMERZ
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Cart, CartItem, Order, OrderItem

logger = logging.getLogger(__name__)

# Helper functions
def get_order_by_transaction(transaction_id):
    try:
        return Order.objects.get(transaction_id=transaction_id)
    except Order.DoesNotExist:
        logger.warning(f"Order with transaction ID {transaction_id} does not exist.")
        return None


def clear_user_cart(user, session):
    """Clears the cart for authenticated or anonymous users."""
    if user.is_authenticated:
        Cart.objects.filter(user=user).delete()
    else:
        session['cart'] = {}


# Views
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


def product_list(request):
    category = request.GET.get('category')
    products = Product.objects.all()

    if category:
        products = products.filter(product_category__name__iexact=category)

    return render(request, 'product_list.html', {
        'products': products,
        'category': category,
    })


def product_search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(product_name__icontains=query) if query else Product.objects.none()

    return render(request, 'search_results.html', {
        'query': query,
        'products': products,
        'no_results': not products.exists() and query,
    })


@login_required
def cart(request):
    try:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_amount = cart.total_amount

        if request.method == 'POST':
            delivery_location = request.POST.get('delivery_location')
            if delivery_location:
                cart.delivery_location = delivery_location
                cart.save()

        return render(request, 'cart.html', {
            'cart': cart,
            'cart_items': cart_items,
            'total_amount': total_amount,
            'is_authenticated': True,
        })
    except Cart.DoesNotExist:
        messages.error(request, "Your cart could not be found.")
        return redirect('product_list')


def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        messages.success(request, f"{product.product_name} added to your cart!")
    else:
        messages.info(request, "Please log in to add products to your cart.")
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    return redirect(request.META.get('HTTP_REFERER', 'product_list'))


@login_required
def remove_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, f"{cart_item.product.product_name} removed from your cart.")
    except CartItem.DoesNotExist:
        logger.warning(f"Remove attempt failed: No CartItem with ID {id} for user {request.user}")
        messages.error(request, "The item you're trying to remove does not exist in your cart.")
    return redirect('cart')


@login_required
def increament_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Quantity of {cart_item.product.product_name} increased.")
    except CartItem.DoesNotExist:
        messages.error(request, "The item you're trying to update does not exist in your cart.")
        logger.warning(f"Increment attempt failed: No CartItem with ID {id} for user {request.user}")
    return redirect('cart')


@login_required
def decreament_cart(request, id):
    try:
        cart_item = CartItem.objects.get(id=id, cart__user=request.user)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
            messages.success(request, f"Quantity of {cart_item.product.product_name} decreased.")
        else:
            cart_item.delete()
            messages.success(request, f"{cart_item.product.product_name} removed from your cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "The item you're trying to update does not exist in your cart.")
        logger.warning(f"Decrement attempt failed: No CartItem with ID {id} for user {request.user}")
    return redirect('cart')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()

        if not cart_items:
            messages.error(request, "Your cart is empty. Add items before proceeding.")
            return redirect('cart')

        if not cart.delivery_location:
            messages.error(request, "Please provide a delivery location in your cart before checking out.")
            return redirect('cart')
        
        order, created = Order.objects.get_or_create(
            user=request.user,
            status='Pending',
            defaults={
                'delivery_location': cart.delivery_location, 
                'total_amount': cart.total_amount
            }
        )

        if created:
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.total_price,
                )

        request.session['order_id'] = order.id

        return redirect('payment_gateway')
    
    except Cart.DoesNotExist:
        messages.error(request, "Your cart could not be found.")
        return redirect('product_list')
    
    except Exception as e:
        logger.error(f"Checkout error for user {request.user}: {e}")
        messages.error(request, "An unexpected error occurred during checkout. Please try again later.")
        return redirect('cart')


@login_required
def payment_gateway(request):
    try:
        user = request.user
        cart = Cart.objects.get(user=user)
        total_amount = cart.total_amount

        TransactionId = str(uuid.uuid4())
        order = Order.objects.create(
            user=user,
            delivery_location=cart.delivery_location,
            total_amount=total_amount,
            status="Pending",
            transaction_id=TransactionId,
        )

        settings = {
            'store_id': settings.SSLCOMMERZ_STORE_ID,
            'store_pass': settings.SSLCOMMERZ_STORE_PASS,
            'issandbox': True,
        }

        sslcz = SSLCOMMERZ(settings)
        post_body = {
            'total_amount': total_amount,
            'currency': "BDT",
            'tran_id': order.transaction_id,
            'success_url': 'http://127.0.0.1:8000/payment_success/',
            'fail_url': 'http://127.0.0.1:8000/payment_fail/',
            'cancel_url': 'http://127.0.0.1:8000/payment_cancel/',
            'cus_name': user.username,
            'cus_email': user.email,
            'cus_phone': "01700000000",
            'cus_add1': "Customer address",
            'cus_city': "Customer city",
            'cus_country': "Bangladesh",
            'shipping_method': "YES",
            'multi_card_name': "",
            'num_of_item': "",
            'product_name': "",
            'product_category': "",
            'product_profile': "general",
        }

        response = sslcz.createSession(post_body)
        return redirect(response['GatewayPageURL'])
    except Exception as e:
        logger.error(f"Payment gateway error: {e}")
        messages.error(request, "Unable to connect to the payment gateway.")
        return redirect('cart')


@csrf_exempt
def payment_success(request):
    transaction_id = request.POST.get('tran_id')
    order = get_order_by_transaction(transaction_id)

    if not order:
        return render(request, 'payment_fail.html', {'error': 'Order not found.'})

    order.status = 'Paid'
    order.save()
    clear_user_cart(request.user, request.session)

    return render(request, 'payment_success.html', {'order': order})


@csrf_exempt
def payment_fail(request):
    transaction_id = request.POST.get('tran_id')
    order = get_order_by_transaction(transaction_id)

    if order:
        order.status = 'Failed'
        order.save()

    return render(request, 'payment_fail.html', {'order': order})


@csrf_exempt
def payment_cancel(request):
    transaction_id = request.POST.get('tran_id')
    order = get_order_by_transaction(transaction_id)

    if order:
        order.status = 'Cancelled'
        order.save()

    return render(request, 'payment_cancel.html', {'order': order})