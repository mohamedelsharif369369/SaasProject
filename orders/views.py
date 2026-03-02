from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem, Order, OrderItem
from commissions.models import Commission
from warehouse.models import Inventory
from django.contrib.auth.decorators import login_required

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(customer=request.user)
    return render(request,'orders/cart.html',{'cart':cart})

@login_required
def add_to_cart(request, product_id):
    cart, _ = Cart.objects.get_or_create(customer=request.user)
    from catalog.models import Product
    product = get_object_or_404(Product,id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart,product=product)
    if not created: item.quantity +=1; item.save()
    return redirect('orders:cart')

@login_required
def remove_from_cart(request,item_id):
    item=get_object_or_404(CartItem,id=item_id)
    item.delete()
    return redirect('orders:cart')

@login_required
def checkout(request):
    cart=get_object_or_404(Cart,customer=request.user)
    if request.method=="POST":
        order=Order.objects.create(customer=request.user,total_amount=cart.total_amount())
        for item in cart.items.all():
            oi=OrderItem.objects.create(order=order,product=item.product,quantity=item.quantity,price=item.product.price)
            inventory=Inventory.objects.filter(product=item.product).first()
            if inventory: inventory.quantity-=item.quantity; inventory.save()
            commission_amount=item.product.price*item.quantity*0.10
            Commission.objects.create(order_item=oi,percentage=10,amount=commission_amount)
        cart.items.all().delete()
        return redirect('orders:cart')
    return render(request,'orders/cart.html',{'cart':cart})
