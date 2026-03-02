from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from catalog.models import Product
from orders.models import OrderItem
from commissions.models import Commission
from warehouse.models import Inventory

@login_required
def seller_dashboard(request):
    if not request.user.is_seller: return render(request,'stores/not_authorized.html')
    products = Product.objects.filter(store__owner=request.user)
    inventory = Inventory.objects.filter(product__in=products)
    order_items = OrderItem.objects.filter(product__in=products)
    commissions = Commission.objects.filter(order_item__product__in=products)
    total_sales=sum(item.price*item.quantity for item in order_items)
    total_commissions=sum(c.amount for c in commissions)
    net_earnings=total_sales-total_commissions
    return render(request,'stores/seller_dashboard.html',{
        'products':products,'inventory':inventory,'order_items':order_items,
        'commissions':commissions,'total_sales':total_sales,
        'total_commissions':total_commissions,'net_earnings':net_earnings})
