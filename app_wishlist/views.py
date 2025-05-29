from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotFound
from app_store.models import DATABASE
from django.contrib.auth import get_user
from logic.control_wishlist import view_in_wishlist, add_to_wishlist, remove_from_wishlist
from django.contrib.auth.decorators import login_required


def wishlist_view(request):
    if request.method == "GET":
        username = get_user(request).username
        data = view_in_wishlist(username)[username]  # получить продукты из избранного для пользователя, используя view_in_wishlist

        products = []
        for product_id in data['products']:
            products.append(DATABASE[product_id])

        return render(request, 'app_wishlist/wishlist.html', context={"products": products})



