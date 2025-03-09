import flet as ft
from config import load_env_file
from auth import AuthManager
from todo import TodoApp

def main(page: ft.Page):
    # Carrega as variáveis de ambiente
    load_env_file()

    # Configurações da página
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE

    # Inicializa o gerenciador de autenticação
    auth_manager = AuthManager(page)

    # Função para iniciar o aplicativo ToDo após o login
    def start_todo_app():
        page.clean()  # Limpa a página atual
        todo_app = TodoApp(page)  # Inicializa o aplicativo ToDo
        page.add(todo_app)  # Adiciona o ToDoApp à página
        page.update()  # Atualiza a página
        todo_app.new_task.focus()  # Foca no campo de nova tarefa

    # Callback para o evento de login
    def on_login(e: ft.LoginEvent):
        if not e.error:
            auth_manager.toggle_login_buttons()  # Atualiza os botões de login/logout
            start_todo_app()  # Inicia o aplicativo ToDo

    # Configura o callback de login
    page.on_login = on_login

    # Adiciona os botões de login e logout à página
    page.add(auth_manager.login_button, auth_manager.logout_button)

# Inicia o aplicativo Flet
ft.app(main, port=8550, view=ft.AppView.WEB_BROWSER, host="localhost", assets_dir="assets")
# ft.app(main, port=3000, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", assets_dir="assets") # Replit