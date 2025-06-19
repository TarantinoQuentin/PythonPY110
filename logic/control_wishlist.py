import json
import os
from app_store.models import DATABASE

PATH_WISHLIST = 'wishlist.json'  # Путь до файла избранного


def view_in_wishlist(username: str = '') -> dict:  # Уже реализовано, не нужно здесь ничего писать
    """
    Просматривает содержимое избранного wishlist.json, если пользователя с именем username нет в избранном, то создает его там

    :param username: Имя пользователя
    :return: Содержимое 'wishlist.json'
    """
    empty_user_wishlist = {'products': []}  # Пустое избранное для пользователя

    if os.path.exists(PATH_WISHLIST):  # Если файл с избранным существует
        with open(PATH_WISHLIST, encoding='utf-8') as f:  # Открываем файл
            wishlist = json.load(f)  # Считываем избранное
            if username not in wishlist:  # Если пользователя нет в избранном, то создаем запись с пустым избранным для него
                wishlist[username] = empty_user_wishlist
    else:  # Если файла с избранным нет
        wishlist = {username: empty_user_wishlist}

    # Запись словаря wishlist в wishlist.json
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:  # Создаём файл и записываем избранное
        json.dump(wishlist, f)

    return wishlist  # Возвращаем содержимое избранного


def add_to_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет продукт в избранное. Если в избранном нет данного продукта, то добавляет его с количеством равное 1.
    Если в избранном есть такой продукт, то добавляет количеству данного продукта + 1.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного добавления, а False в случае неуспешного добавления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)  # Помните, что у вас есть уже реализация просмотра избранного view_in_wishlist(username),
    # поэтому, чтобы загрузить данные из избранного, не нужно заново писать код.
    if id_product not in DATABASE:
        return False
    # Проверьте существует ли добавляемый товар с id_product в базе данных DATABASE, если нет, то возвращаем False,
    #  так как добавление в избранное прошло неуспешно.

    user_wishlist = wishlist[username]["products"]  # в переменную user_wishlist запишите данные об товарах пользователя.
    #  Т.е. в user_wishlist будет словарь из ключа "products" для соответствующего пользователя по username.

    # ! Обратите внимание, что в переменной wishlist под ключом значения username находится словарь с ключом "products".
    # ! Именно в wishlist[username]["products"] лежит список где по id продуктов можно получить число продуктов в избранном.
    # ! Т.е. чтобы обратиться к продукту с id_product = "1" в переменной wishlist нужно вызвать
    # ! wishlist[username]["products"][id_product]
    # ! Далее уже сами решайте, как и в какой последовательности дальше действовать.

    # Проверьте, а существует ли товар с id_product в избранном пользователя user_wishlist, если товар существует,
    #  то увеличиваем его количество в user_wishlist на 1, иначе товар добавляется в первый раз и его количество равно 1.
    if id_product not in user_wishlist:
        user_wishlist.append(id_product)

    # Не забываем записать обновленные данные wishlist в 'wishlist.json'. Так как именно из этого файла мы считываем данные
    #  и если мы не запишем изменения, то считать измененные данные затем не получится. Так user_wishlist является частью
    #  словаря wishlist, то любые изменения в user_wishlist аналогично отражаются в wishlist, поэтому достаточно записать
    #  в 'wishlist.json' словарь из wishlist
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)

    return True


def remove_from_wishlist(id_product: str, username: str = '') -> bool:
    """
    Добавляет позицию продукта из избранного. Если в избранном есть такой продукт, то удаляется ключ в словаре
    с этим продуктом.

    :param id_product: Идентификационный номер продукта в виде строки.
    :param username: Имя пользователя

    :return: Возвращает True в случае успешного удаления, а False в случае неуспешного удаления(товара по id_product
    не существует).
    """
    wishlist = view_in_wishlist(username)  # Помните, что у вас есть уже реализация просмотра избранного view_in_wishlist(username),
    # поэтому, чтобы загрузить данные из избранного, не нужно заново писать код.

    # С переменной user_wishlist функции remove_from_wishlist ситуация аналогичная, что с wishlist функции add_to_wishlist
    user_wishlist = wishlist[username]["products"]  # в переменную user_wishlist запишите данные об товарах пользователя.
    #  Т.е. в user_wishlist будет словарь из ключа "products" для соответствующего пользователя по username.

    # Проверьте, существует ли товар с id_product в избранном пользователя user_wishlist, если нет, то возвращаем False.
    if id_product not in user_wishlist:
        return False
    else:
        user_wishlist.remove(id_product)
    # Если существует товар, то удаляем ключ 'id_product' у user_wishlist,
    #  вспомните как удалять ключи у словаря.

    # Не забываем записать обновленные данные wishlist в 'wishlist.json', аналогично как делали в add_to_wishlist
    with open(PATH_WISHLIST, mode='w', encoding='utf-8') as f:
        json.dump(wishlist, f)
    return True


if __name__ == "__main__":
    # Проверка работоспособности функций view_in_wishlist, add_to_wishlist, remove_from_wishlist
    if os.path.exists('wishlist.json'):  # Если файл существует
        os.remove('wishlist.json')  # Удаляем избранное

    print('Проверяем избранное', "Ответ:     {'': {'products': []}}", f'Результат: {view_in_wishlist()}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_wishlist("1")}\n', sep='\n')
    print('Добавляем товар с id = 0', 'Ответ:     False', f'Результат: {add_to_wishlist("0")}\n', sep='\n')
    print('Добавляем товар с id = 1', 'Ответ:     True', f'Результат: {add_to_wishlist("1")}\n', sep='\n')
    print('Добавляем товар с id = 2', 'Ответ:     True', f'Результат: {add_to_wishlist("2")}\n', sep='\n')
    print('Проверяем избранное', "Ответ:     {'': {'products': ['1', '2']}}", f'Результат: {view_in_wishlist()}\n', sep='\n')
    print('Удаляем товар с id = 0', "Ответ:     False", f'Результат: {remove_from_wishlist("0")}\n', sep='\n')
    print('Удаляем товар с id = 1', "Ответ:     True", f'Результат: {remove_from_wishlist("1")}\n', sep='\n')
    print('Проверяем избранное', "Ответ:     {'': {'products': ['2']}}", f'Результат: {view_in_wishlist()}\n', sep='\n')

    if os.path.exists('wishlist.json'):  # Если файл существует
        os.remove('wishlist.json')  # Удаляем избранное
