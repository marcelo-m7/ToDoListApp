import flet as ft
from flet.auth.providers import GitHubOAuthProvider
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv, set_key
import json


class Task(ft.Column):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete
        self.display_task = ft.Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = ft.TextField(expand=1)

        self.display_view = self._display_view()
        self.edit_view = self._edit_view()
        self.controls = [self.display_view, self.edit_view]

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.task_name = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
        self.task_status_change(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

    def delete_clicked(self, e):
        self.task_delete(self)

    def _display_view(self):
        return ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.display_task,
                ft.Row(
                    spacing=0,
                    controls=[
                        ft.IconButton(
                            icon=ft.Icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        ft.IconButton(
                            ft.Icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )
   
    def _edit_view(self):
        return ft.Row(
            visible=False,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                self.edit_name,
                ft.IconButton(
                    icon=ft.Icons.DONE_OUTLINE_OUTLINED,
                    icon_color=ft.Colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )
    
class TodoApp(ft.Column):
    def __init__(self, page):
        load_dotenv()
        super().__init__()
        self.page = page
        self.new_task = ft.TextField(
            hint_text="What needs to be done?", on_submit=self.add_clicked, expand=True
        )
        self.tasks = ft.Column()
        self.filter = ft.Tabs(
            scrollable=False,
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[ft.Tab(text="all"), ft.Tab(text="active"), ft.Tab(text="completed")],
        )

        self.items_left = ft.Text("0 items left")
        self.width = 600
        self.controls = self._controls()
        self.load_tasks()

    def add_clicked(self, e):
        if self.new_task.value.strip():
            task = Task(self.new_task.value, self.task_status_change, self.task_delete)
            self.tasks.controls.append(task)
            self.new_task.value = ""
            self.new_task.focus()
            self.update()
            self.save_tasks()

    def task_status_change(self, task):
        self.update()
        self.save_tasks()

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()
        self.save_tasks()

    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)
        self.save_tasks() 
        
    def before_update(self):
        status = self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible = (
                status == "all"
                or (status == "active" and task.completed == False)
                or (status == "completed" and task.completed)
            )
            if not task.completed:
                count += 1
        self.items_left.value = f"{count} active item(s) left"
  
    def load_encryption_key(self):
        key = os.getenv("FERNET_KEY")
        
        if not key:
            print("FERNET_KEY not found in environment variables. Checking .env file...")
            
            if not os.path.exists("src/.env"):
                print(".env file not found. Generating a new key...")
                key = Fernet.generate_key().decode()
                set_key(".env", "FERNET_KEY", key)
                print(f"New FERNET_KEY generated and saved to .env: {key}")
            else:
                with open(".env", "r") as f:
                    for line in f:
                        if line.startswith("FERNET_KEY="):
                            key = line.split("=", 1)[1].strip()
                            break
                
                if not key:
                    print("FERNET_KEY not found in .env file. Generating a new key...")
                    key = Fernet.generate_key().decode()
                    set_key(".env", "FERNET_KEY", key)
                    print(f"New FERNET_KEY generated and saved to .env: {key}")
        
        return key

    def save_tasks(self):
        tasks_data = []
        for task in self.tasks.controls:
            tasks_data.append({
                "name": task.task_name,
                "completed": task.completed
            })
        tasks_data_json = json.dumps(tasks_data).encode()
        tasks_data_encrypted = Fernet(self.load_encryption_key()).encrypt(tasks_data_json)
        self.page.client_storage.set("tasks", tasks_data_encrypted.decode())

    def load_tasks(self):
        tasks_data_encrypted = self.page.client_storage.get("tasks")
        if tasks_data_encrypted:
            try:
                tasks_data_json = Fernet(self.load_encryption_key()).decrypt(tasks_data_encrypted.encode())
                tasks_data = json.loads(tasks_data_json.decode())
                for task_data in tasks_data:
                    task = Task(task_data["name"], self.task_status_change, self.task_delete)
                    task.completed = task_data["completed"]
                    task.display_task.value = task_data["completed"]
                    self.tasks.controls.append(task)
            except Exception as e:
                print("Error decrypting tasks:", e)
                self.page.client_storage.remove("tasks")

    def _controls(self):
        return [
            ft.Row(
                [ft.Text(value="Todos", theme_style=ft.TextThemeStyle.HEADLINE_MEDIUM)],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                controls=[
                    self.new_task,
                    ft.FloatingActionButton(
                        icon=ft.Icons.ADD, on_click=self.add_clicked
                    ),
                ],
            ),
            ft.Column(
                spacing=25,
                controls=[
                    self.filter,
                    self.tasks,
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        controls=[
                            self.items_left,
                            ft.OutlinedButton(
                                text="Clear completed", on_click=self.clear_clicked
                            ),
                        ],
                    ),
                ],
            ),
        ]

def load_env_file(env_file_path="src/.env"):
    load_dotenv()
    try:
        with open(env_file_path, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()

                    if (value.startswith('"') and value.endswith('"')) or (
                        value.startswith("'") and value.endswith("'")
                    ):
                        value = value[1:-1]

                    os.environ[key] = value
                    print(f"Variável de ambiente definida: {key}={os.environ[key]}")
    except FileNotFoundError:
        print(f"Arquivo {env_file_path} não encontrado.")
    except Exception as e:
        print(f"Erro ao carregar o arquivo .env: {e}")


def start_todo_app(page: ft.Page):
    page.title = "ToDo App"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.update()
    todo_app = TodoApp(page)
    page.add(todo_app)
    page.update()
    todo_app.new_task.focus()
    
def main(page: ft.Page):
    # page.client_storage.clear()    
    provider = GitHubOAuthProvider(
        client_id=os.getenv("GITHUB_CLIENT_ID"),
        client_secret=os.getenv("GITHUB_CLIENT_SECRET"),
        redirect_url='http://localhost:8550/oauth_callback',
    )

    def login_button_click(e):
        page.login(provider, scope=["public_repo"])

    def on_login(e: ft.LoginEvent):
        if not e.error:
            toggle_login_buttons()
            start_todo_app(page)

    def logout_button_click(e):
        page.logout()

    def on_logout(e):
        toggle_login_buttons()

    def toggle_login_buttons():
        login_button.visible = page.auth is None
        logout_button.visible = page.auth is not None
        page.update()

    login_button = ft.ElevatedButton("Login with GitHub", on_click=login_button_click)
    logout_button = ft.ElevatedButton("Logout", on_click=logout_button_click)
    toggle_login_buttons()
    page.on_login = on_login
    page.on_logout = on_logout
    page.add(login_button, logout_button)

load_env_file()
ft.app(main, port=8550, view=ft.AppView.WEB_BROWSER)
