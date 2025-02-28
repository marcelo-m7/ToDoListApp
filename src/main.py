import flet as ft
from todo import TodoApp
from storage import storage

def set_app_config(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page

def main(page: ft.Page):
    set_app_config(page)
    storage(page)
    page.add(TodoApp())


ft.app(main)