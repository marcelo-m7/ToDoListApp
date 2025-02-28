import flet as ft


def storage(page: ft.Page):
    # strings
    page.client_storage.set("key", "value")

    # numbers, booleans
    page.client_storage.set("number.setting", 12345)
    page.client_storage.set("bool_setting", True)

    # lists
    page.client_storage.set("favorite_colors", ["red", "green", "blue"])
