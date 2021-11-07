from django.shortcuts import render

# Create your views here.
from .models import Canteen, Shop


def show_canteen(request):
    template_name = 'canteen/canteen_list.html'
    context = {'canteen_list': Canteen.objects.all()}
    return render(request, template_name, context)


def show_shop(request):
    template_name = 'canteen/shop_list.html'
    context = {
        'canteen_with_shop_list': Canteen.objects.all(),
        'shop_list': Shop.objects.all()
    }
    return render(request, template_name, context)
