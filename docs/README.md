# ToDo List App

Este é um aplicativo de lista de tarefas (ToDo List) desenvolvido por Marcelo Santos (a79433) para diciplina de Computação Móvel. O aplicativo foi desenvolvido em Python com o uso da diblioteca Flet e está configurado para Deploy em Replit, com porta aberta 3000. A app permite autenticação via GitHub e armazena as tarefas de forma segura usando criptografia.

## Pré-requisitos

1. **Python**: Certifique-se de que o Python 3.8 ou superior está instalado.
2. **GitHub OAuth App**: Crie um OAuth App no GitHub para obter as credenciais necessárias (`GITHUB_CLIENT_ID` e `GITHUB_CLIENT_SECRET`).

## Configuração

### 1. Criar o arquivo `.env`

Crie um arquivo `.env` dentro da pasta `src/` com as seguintes variáveis:

```plaintext
GITHUB_CLIENT_ID="seu_client_id_aqui"
GITHUB_CLIENT_SECRET="seu_client_secret_aqui"
FERNET_KEY=""  # Opcional (será gerado automaticamente se não existir)
```

### 2. Configurar host (`src/auth.py` e `src/main.py`)

 Caso se pretenda fazer deploy em Replit, é nessário alterar a URL e porta palas fornecidas pelo servidor.
 `src/auth.py.`:
```python
redirect_url='http://localhost:3000/oauth_callback',
# redirect_url='https://9add73eb-1d78-4beb-99c1-ddcc8e613ebd-00-2c518dp4o8er8.riker.replit.dev:3000/oauth_callback', # Replit

```

`src/main.py`:
```python
ft.app(main, port=8550, view=ft.AppView.WEB_BROWSER, host="localhost", assets_dir="src/assets")
# ft.app(main, port=3000, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", assets_dir="src/assets") # Replit
```