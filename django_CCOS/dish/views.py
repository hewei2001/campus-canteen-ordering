from django.shortcuts import render
from .models import Shop, Dish, Orders
from customer.models import Customer
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.


def show_dish(request):
    template_name = 'dish/dish_list.html'
    context = {
        'shop_with_dish_list': Shop.objects.all(),
        'dish_list': Dish.objects.all(),
    }

    return render(request, template_name, context)


def show_order(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "请先登录顾客账户~")
        return redirect('/customer/login/')

    template_name = 'dish/my_order.html'

    user_id = request.session['user_id']

    context = {
        'order_list': Orders.objects.filter(customer_id=user_id),
    }
    return render(request, template_name, context)


def get_order(request, dish_id):
    dish = get_object_or_404(Dish, dish_id=dish_id)
    user_id = request.session['user_id']

    try:
        user = Customer.objects.filter(customer_id=user_id).first()
        order = Orders.objects.create(dish=dish, customer=user)
        order.order_price = order.dish.dish_price
        order.order_status = 0
        order.save()
        messages.success(request, '下单成功，订单号为 (Order ID-{}). 请支付 {} 元'.format(order.order_id, order.order_price))
        return redirect("dish:show_order")

    except ObjectDoesNotExist:
        messages.warning(request, "你还没有订单哦~")
        return redirect("dish:show_order")
