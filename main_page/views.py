from django.shortcuts import render, redirect
from django.http import HttpResponse
import telebot

bot = telebot.TeleBot('5732506869:AAGHKm66TrF6-ca20GnvqxIgOrDOPkl65LY')

from . import models


def home_page(request):
    get_all_category = models.Category.objects.all()

    return render(request, 'index.html',
                  {'all_category': get_all_category})


# Получить все товары и вывод их на front
def get_all_products(request):
    all_products = models.Product.objects.all() #Получить все

    return render(request, 'product.html',
                  {'all_products': all_products})


# Получение опеределенного товара
def get_exact_product(request, pk):
    current_product = models.Product.objects.get(product_name=pk)

    return render(request, 'exact_product.html',
                  {'current_product': current_product}) # ! Передать на front


# Получение конкретной категории
def get_exact_category(request, pk):
    current_category = models.Category.objects.get(id=pk)

    category_products = models.Product.objects.filter(product_category=current_category) # Выводим продукты

    return render(request, 'exact_category.html',
                  {'category_products': category_products})


def search_exact_product(request):
    if request.method == 'POST':
        get_product = request.POST.get('search_product')

        try:
            models.Product.objects.get(product_name=get_product)

            return redirect(f'/product/{get_product}')

        except:
            return redirect('/')


#Добавление в корзину
def add_product_to_user_cart(request, pk):
    if request.method == 'POST':
        checker = models.Product.objects.get(id=pk)
        if checker.product_count >= int(request.POST.get('pr_count')):
            models.UserCart.objects.create(user_id=request.user.id,
                                           user_product=checker,
                                           user_product_quantity=int(request.POST.get('pr_count'))).save()

            return redirect('/products')

        else:
            return redirect(f'/product/{checker.product_name}')


#Вывод корзины пользователя
def get_exact_user_cart(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)

    return render(request, 'user_cart.html', {'user_cart': user_cart})


#Удаление продукта из корзины
def delete_exact_user_cart(request, pk):
    product_to_delete = models.Product.objects.get(id=pk)

    models.UserCart.objects.filter(user_id=request.user.id,
                                user_product=product_to_delete).delete()

    return redirect('/user_cart')


def accept_order(request):
    user_cart = models.UserCart.objects.filter(user_id=request.user.id)
    admin_id = 650245882
    total = 0
    message = 'новый заказ\n\n'

    for k in user_cart:
        message += f'{k.user_product.product_name} : {k.user_product_quantity}' \
                   f' шт : {round(k.user_product_quantity*k.user_product.product_price)} сум\n'
        total += k.user_product_quantity*k.user_product.product_price
        message += f'на общую сумму в {total} sum'
        bot.send_message(admin_id, message)
        models.UserCart.objects.filter(user_id=request.user.id).delete()

        return render(request, 'user_cart.html')
