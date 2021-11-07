from django.shortcuts import render, redirect, HttpResponseRedirect, reverse
from django.core.paginator import Paginator
from django.http import JsonResponse
from .forms import LoginForm, RegisterForm, AddressForm
from django.contrib import messages

from .models import Customer, Address


def register(request):
    register_form = RegisterForm()
    if request.session.get('is_login', None):  # 不允许重复登录
        return render(request, 'customer/index.html', locals())  # 自动跳转到首页
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 获取数据
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            tel = register_form.cleaned_data['tel']

            if password1 != password2:  # 判断两次密码是否相同
                print("[DEBUG][POST][STATE]:两次输入的密码不同！")
                # message = "两次输入的密码不同！"
                return render(request, 'customer/register.html', locals())
            else:
                same_id_cus = Customer.objects.filter(customer_name=username)
                # same_id_mng = StoreManager.objects.filter(manager_name=username)
                if same_id_cus:  # 用户名唯一
                    message = '顾客用户名已经存在~请换一个'
                    return render(request, 'customer/register.html', locals())
                # 当一切都OK的情况下，创建新用户
                else:
                    new_cus = Customer.objects.create(customer_name=username, customer_tel=tel,
                                                      customer_password=password1)
                    new_cus.save()
                    # 自动跳转到登录页面
                    login_form = LoginForm()
                    message = "注册成功！"
                    return render(request, 'customer/login.html', locals())  # 自动跳转到登录页面
    else:
        return render(request, 'customer/register.html', locals())

    return render(request, 'customer/register.html', locals())


def login(request):
    login_form = LoginForm()
    if request.session.get('is_login', None):
        print("[DEBUG][POST][STATE]:已经登陆")
        return render(request, 'customer/index.html', locals())

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        message = "请检查填写的内容！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            # identy 表示
            print("[DEBUG][POST][LOGIN][username]:{}".format(username))
            print("[DEBUG][POST][LOGIN][password]:{}".format(password))
            try:
                print("[DEBUG][POST][STATE]:查询顾客用户数据库")
                user_cus = Customer.objects.get(customer_name=username)
                if user_cus.customer_password == password:
                    print("[DEBUG][POST][USERNAME]:{}".format(user_cus.customer_name))
                    print("[DEBUG][POST][STATE]:登录成功")
                    messages.success(request, '{}登录成功！'.format(user_cus.customer_name))
                    user_cus.customer_status = 1
                    user_cus.save()
                    request.session['is_login'] = True
                    request.session['user_id'] = user_cus.customer_id
                    request.session['user_name'] = user_cus.customer_name
                    request.session['tel'] = user_cus.customer_tel
                    return render(request, 'customer/index.html', locals())
                else:
                    print("[DEBUG][POST][STATE]:密码不正确")
                    message = "密码不正确"
            except:
                print("[DEBUG][POST][STATE]:用户不存在")
                message = "用户不存在"
    return render(request, 'customer/login.html', locals())


def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return render(request, 'customer/index.html', locals())
    user_id = request.session['user_id']
    print("[DEBUG][REQUEST][退出]]")
    print("[DEBUG][REQUEST][USER_ID]:{}".format(user_id))
    try:
        user = Customer.objects.get(customer_id=user_id)
        print("[DEBUG][REQUEST][退出]]：退出顾客身份")
        user.customer_status = 0  # 更新离线状态
        user.save()
    except:
        print("[DEBUG][request][STATE]:退出错误，无法更新数据库中用户状态")

    request.session.flush()
    return render(request, 'customer/index.html', locals())


def information(request):
    if not request.session.get('is_login', None):
        messages.warning(request, "请先登录顾客账户~")
        return redirect('/customer/login/')

    address_form = AddressForm()
    user_id = request.session['user_id']
    customer = Customer.objects.filter(customer_id=user_id).first()

    if customer.address:
        # print("已经填过地址")
        return redirect("customer:show_info")

    if request.method == "POST":
        address_form = AddressForm(request.POST)
        if address_form.is_valid():
            new_district = address_form.cleaned_data['district']
            new_building = address_form.cleaned_data['building']
            new_room = address_form.cleaned_data['room']
            try:
                # 匹配当前用户号
                cus_info = Address.objects.create(district=new_district, building=new_building, room=new_room)
                cus_info.save()
                customer = Customer.objects.filter(customer_id=user_id).first()
                customer.Address = Address.objects.all().first()
                customer.save()
                request.session['district'] = new_district
                request.session['building'] = new_building
                request.session['room'] = new_room
                messages.success(request, '个人地址添加成功！')
                return render(request, 'customer/show_info.html', locals())
            except:
                messages.warning(request, '个人地址添加失败')
                return render(request, 'customer/information.html', locals())

    return render(request, 'customer/information.html', locals())


def show_info(request):
    return render(request, 'customer/show_info.html')
