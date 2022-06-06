from django.shortcuts import render
from django.http import HttpResponse
from menu.models import Categories
import json
import os
from VladlinkProject.settings import BASE_DIR


def export_to_type_a():
    """Разработать фунĸционал по эĸспорту данных ĸатегорий в файл (например type_a.txt )
    по следующей струĸтуре:
    [ОТСТУП][Название категории][Пробел][URL от корня до категории]
    Пользователи /users
        Создание /users/create
        Список /users/list
            Активные /users/list/active
            Удаленные /users/list/deleted
        Поиск /users/search
    Заявки /requests
        Заявки на подкючение /requests/connecting"""

    def create_str_for_tree(list_for_row: dict, tree: dict, text: str):
        print(f"Вход, list_for_row = {list_for_row}")

        if list_for_row['level'] == 0:
            print('Входи, если level = 0', list_for_row)
            text += f"{list_for_row['name']} /{list_for_row['alias']}\n"
            # print(text)
        else:
            # print(list_for_row)
            level_item = list_for_row['level']
            temp = list_for_row['parent_id']
            while level_item > 0:
                for i in tree:
                    if i['level'] == level_item and i['id'] == temp:
                        temp = i['id']
                        print('Перебираем в цикле', i)
                        level_item -= 1
            # не работает
            # for i in range(list_for_row['level'] + 1):
            #     print('level = ', i, ' ,', list_for_row)
            #     id = [k for k in tree if k['level'] == i and (list_for_row['parent_id']==k['id'])]
            # print(id)

            # for i in range(list_for_row['level']):
            #     if tree['level'] == i and tree[1]['id'] == list_for_row['parent_id']:
            #         print(list_for_row)

            # i = [k for k in tree if k['tree_id']==1]
            # print(i)

            text += f"{list_for_row['name']} /{list_for_row['alias']}\n"
            # print(text)
        # for i in list_for_row:
        #     if i['parent_id'] is None:

        # list_row = []
        # text = ''
        # for i in list_for_row:
        #     if i['parent_id'] is None:
        #         text = [f"{text*number_of_spaces}{i['name']} /{i['alias']}"]
        #         list_row.extend(text)
        #     else:
        #         pass
        # print(list_row)
        # text_for_type_a += list_for_row['alias']

    data_folder = os.path.join(BASE_DIR, 'type_a.txt')
    all_categories = [i for i in Categories.objects.all().values()]
    # определяем количество tree_id
    max_tree = sorted(all_categories, key=lambda d: d['tree_id'], reverse=True)[0]['tree_id']
    # Выбираем каждое дерево сортируя по возростанию дерева
    for i in range(1, max_tree + 1):
        tree = sorted([j for j in all_categories if j['tree_id'] == i], key=lambda d: d['lft'])
        for j in tree:
            text = ''
            create_str_for_tree(j, tree, text)


    # create_row(all_categories)
    row = ''
    # with open(data_folder, "w") as write_to_type_a:
    #     pass
    #     write_to_type_a.write()

export_to_type_a()