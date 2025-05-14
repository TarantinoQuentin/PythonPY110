from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:  # TODO Если id_ было передано (существует)
            if id_ in DATABASE:  # TODO Если этот id_ есть в базе (DATABASE), то вернуть JsonResponse товара (словаря с характеристиками товара)
                data = DATABASE[id_]
            else:
                raise HttpResponseNotFound("Данного продукта нет в базе данных")  # TODO Иначе вернуть HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            data = DATABASE
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                 'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ
