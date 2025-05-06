from django.shortcuts import render
from weather_api import current_weather
from django.http import JsonResponse


def weather_view(request):
    if request.method == "GET":
        data = current_weather(lat=59.93, lon=30.31)
        return JsonResponse(data, json_dumps_params={'ensure_ascii': False,
                                                     'indent': 4})
