from django.shortcuts import render

from django.http import JsonResponse
from .models import DATABASE


def product_view_json(request):
    if request.method == "GET":
        return JsonResponse(DATABASE, json_dumps_params={'ensure_ascii': False,
                                                         'indent': 4})
