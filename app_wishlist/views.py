from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from django.contrib.auth import get_user
from logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth.decorators import login_required


@login_required(login_url='app_login:login_view')
def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username]  # получить продукты из избранного для пользователя, используя view_in_wishlist

        products = []
        for product_id in data['products']:
            products.append(DATABASE[product_id])

        return render(request, 'app_wishlist/wishlist.html', context={"products": products})


@login_required(login_url='app_login:login_view')
def wishlist_view_json(request):
    """
    Просмотр всех продуктов в избранном для пользователя и возвращение этого в JSON
    """
    if request.method == "GET":
        username = get_user(request).username  # from django.contrib.auth import get_user
        data = view_in_wishlist(username)[username]  # получите данные о списке товаров в избранном у пользователя view_in_wishlist(username)[username]
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})


@login_required(login_url='app_login:login_view')
def wishlist_add_view_json(request, id_product: str):
    """
    Добавление продукта в избранное и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = add_to_wishlist(id_product, username)  # вызовите обработчик add_to_wishlist(id_product, username) добавляющий продукт
        if result:
            return JsonResponse({"answer": "Продукт успешно добавлен в избранное"},
                                json_dumps_params={'ensure_ascii': False})  # верните JsonResponse с ключом "answer" и значением "Продукт успешно добавлен в избранное"

        return JsonResponse({"answer": "Неудачное добавление в избранное"}, status=404,
                            json_dumps_params={'ensure_ascii': False})  # верните JsonResponse с ключом "answer" и значением "Неудачное добавление в избранное" и параметром status=404


@login_required(login_url='app_login:login_view')
def wishlist_del_view_json(request, id_product: str):
    """
    Удаление продукта из избранного и возвращение информации об успехе или неудаче в JSON
    """
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product, username)  # вызовите обработчик remove_from_wishlist(id_product, username) удаляющий продукт из избранного
        if result:
            return JsonResponse({"answer": "Продукт успешно удален из избранного"},
                                json_dumps_params={'ensure_ascii': False})  # верните JsonResponse с ключом "answer" и значением "Продукт успешно удалён из избранного"

        return JsonResponse({"answer": "Неудачное удаление из избранного"}, status=404,
                            json_dumps_params={'ensure_ascii': False})  # верните JsonResponse с ключом "answer" и значением "Неудачное удаление из избранного" и параметром status=404


@login_required(login_url='app_login:login_view')
def wishlist_del_view(request, id_product):
    if request.method == "GET":
        username = get_user(request).username
        result = remove_from_wishlist(id_product, username)  # Вызвать функцию удаления из корзины
        if result:
            return redirect("app_wishlist:wishlist_view")  # Вернуть перенаправление на корзину

        return HttpResponseNotFound("Неудачное удаление из избранного")