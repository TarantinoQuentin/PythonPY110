from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from logic.control_cart import view_in_cart


def login_view(request):
    if request.method == "GET":
        return render(request, "login/login.html")

    if request.method == "POST":
        data = request.POST  # Получаем данные из post запроса
        user = authenticate(username=data["username"], password=data["password"])  # Понимаем, что за пользователь перед нами
        view_in_cart(user.username)  # Получаем корзину пользователя, если её нет, то создаем её
        if user:  # Если пользователь есть в базе
            login(request, user)  # Авторизируем пользователя
            return redirect("/")  # Перенаправляем пользователя на стартовую страницу
        # Иначе заново показываем форму авторизации
        return render(request, "login/login.html", context={"error": "Неверные данные"})


def logout_view(request):
    if request.method == "GET":
        logout(request)  # Функция разлогинивает пользователя
        return redirect("/") # Верните редирект на стартовую страницу