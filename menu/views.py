from django.shortcuts import render
from .models import Categories
from VladlinkProject.settings import BASE_DIR
from django.db import connection

import json
import os


def export_to_type_a():
    """Разработать фунĸционал по эĸспорту данных ĸатегорий в файл (например type_a.txt )"""

    def create_str_for_tree(list_for_row: dict, tree: list, text: str):
        """ Создание/возврат строки типа:
        [ОТСТУП][Название категории][Пробел][URL от корня до категории]
        [ОТСТУП][Название категории]"""

        start_name = list_for_row['name']
        step_slesh = list_for_row['level'] + 1
        start_alias = '/'
        step_alias = ''
        for i in tree:
            if i['parent_id'] == None:
                start_alias = i['alias']

        if list_for_row['level'] == 0:
            text += list_for_row['name'] + ' ' + list_for_row['alias'] + '/\n'
            start_alias = '/' + list_for_row['alias']
        else:
            temp_level = list_for_row['level']
            temp_parent = list_for_row['parent_id']
            while temp_level > 0:
                for i in tree:
                    if i['id'] == temp_parent:
                        text += '/' + i['alias'] + '/' + list_for_row['alias'] + text + "\n"
                        temp_parent = i['id']
                        step_alias = list_for_row['alias'] + '/' + step_alias
                        temp_level = temp_level - 1
                        list_for_row = i
                        break

        return {'name': f"{' ' * step_slesh} {start_name}", 'alias': f"{start_alias}/{step_alias}"}

    result_list = []
    data_folder_a = os.path.join(BASE_DIR, 'type_a.txt')
    data_folder_b = os.path.join(BASE_DIR, 'type_b.txt')
    all_categories = [i for i in Categories.objects.all().values()]
    # определяем количество tree_id
    max_tree = sorted(all_categories, key=lambda d: d['tree_id'], reverse=True)[0]['tree_id']
    # Выбираем каждое дерево сортируя по возростанию
    text = ''
    for i in range(1, max_tree + 1):
        tree = sorted([j for j in all_categories if j['tree_id'] == i], key=lambda d: d['lft'])
        for j in tree:
            result_list.append(create_str_for_tree(j, tree, text))
    text_for_a = ''
    text_for_b = ''

    for i in result_list:
        text_for_a += i['name'] + ' ' + i['alias'] + '\n'
        text_for_b += i['name'] + '\n'
    print(text_for_a)
    print(text_for_b)

    with open(data_folder_a, "w") as write_to_type_a:
        write_to_type_a.write(text_for_a)

    with open(data_folder_b, "w") as write_to_type_b:
        write_to_type_b.write(text_for_b)


def create_categories(data: dict, i: int, parent=None):
    """ Рекурсивный метод добавления категорий в БД"""
    if data[i].get('childrens') == None:
        Categories.objects.create(id=data[i].get('id'), name=data[i].get('name'), alias=data[i].get('alias'),
                                  parent=parent)
    if data[i].get('childrens'):
        childrens = data[i].get('childrens')
        parent = Categories.objects.create(id=data[i].get('id'), name=data[i].get('name'),
                                           alias=data[i].get('alias'), parent=parent)
        for j in range(len(childrens)):
            create_categories(childrens, j, parent)


def menu(request):
    """ Отображение меню, категории которого взяты с json по пути BASE_DIR + categories_old.json"""
    cursor = connection.cursor()
    cursor.execute("delete from menu_categories")

    data_folder = os.path.join(BASE_DIR, 'categories_old.json')
    with open(data_folder, 'r') as read_vladlink_json:
        data = json.load(read_vladlink_json)

        for i in range(len(data)):
            create_categories(data, i)

    export_to_type_a()
    return render(request, 'menu/menu.html', {'Categories': Categories.objects.all(), 'data': data})
