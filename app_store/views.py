from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound
from .models import DATABASE
from logic.services import filtering_category


def product_view_json(request):
    if request.method == "GET":
        id_ = request.GET.get('id')
        if id_:  # Если id_ было передано (существует)
            if id_ in DATABASE:  # Если этот id_ есть в базе (DATABASE), то вернуть JsonResponse товара (словаря с характеристиками товара)
                data = DATABASE[id_]
            else:
                return HttpResponseNotFound("Данного продукта нет в базе данных")  # Иначе вернуть HttpResponseNotFound("Данного продукта нет в базе данных")
        else:
            data = DATABASE
    # Обработка фильтрации из параметров запроса
    category_key = request.GET.get("category")  # Считали 'category'
    if ordering_key := request.GET.get("ordering"):  # Если в параметрах есть 'ordering'
        reverse = request.GET.get("reverse")
        if reverse and reverse.lower() == 'true':  # Если в параметрах есть 'ordering' и 'reverse'=True
            data = filtering_category(DATABASE, category_key, ordering_key, reverse=True)  # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=True
        else:  # Если не обнаружили в адресно строке ...&reverse=true , значит reverse=False
            data = filtering_category(DATABASE, category_key, ordering_key, reverse)   # TODO Использовать filtering_category и провести фильтрацию с параметрами category, ordering, reverse=False
    else:
        data = filtering_category(DATABASE, category_key)   # TODO Использовать filtering_category и провести фильтрацию с параметрами category
    # В этот раз добавляем параметр safe=False, для корректного отображения списка в JSON
    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False,
                                                             'indent': 4})


def shop_view(request):
    if request.method == "GET":
        with open('app_store/shop.html', encoding="utf-8") as f:
            data = f.read()  # Читаем HTML файл
        return HttpResponse(data)  # Отправляем HTML файл как ответ


def product_page_view(request, page):
    if request.method == "GET":
        if isinstance(page, str):  # Проверяем, что в параметр page передали значение строкового типа
            for data in DATABASE.values():  # Перебираем все товары (словари) в DATABASE
                if data['html'] == page:  # Если значение переданного параметра совпадает именем html файла, получаемого по ключу
                    with open(f'app_store/product/{page}.html', encoding="utf-8") as f:
                        page_data = f.read()
                    return HttpResponse(page_data)
            # Если за всё время поиска не было совпадений, то значит по данному имени нет соответствующей
            # страницы товара и можно вернуть ответ с ошибкой HttpResponse(status=404)
        elif isinstance(page, int):  # Ветка для обработки типа int
            data = DATABASE.get(str(page))  # Получаем какой странице соответствует данный id
            if data:  # Если по данному page было найдено значение
                with open(f'app_store/product/{data["html"]}.html',
                          encoding="utf-8") as f:  # Определяем название файла для открытия
                    return HttpResponse(f.read())

        return HttpResponse(status=404)
