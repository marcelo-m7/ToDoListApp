# ToDo List App

Este é um aplicativo de lista de tarefas (ToDo List) desenvolvido por Marcelo Santos (a79433) para a disciplina de Computação Móvel da Universidade do Algarve (UAlg). O aplicativo foi desenvolvido em Python utilizando a biblioteca Flet e está configurado para deploy no Replit, com a porta aberta 3000. A aplicação permite autenticação via GitHub e armazena as tarefas de forma segura usando criptografia.

## Requisitos

1. **Python**: Certifique-se de que o Python 3.8 ou superior está instalado.
2. **Dependências**: Instale as bibliotecas necessárias utilizando o arquivo `docs/requirements.txt`.
3. **GitHub OAuth App**: Crie um OAuth App no GitHub para obter as credenciais necessárias (`GITHUB_CLIENT_ID` e `GITHUB_CLIENT_SECRET`).

## Instalação

Para instalar as dependências do projeto, execute o seguinte comando no terminal dentro do ambiente virtual:

```sh
pip install -r docs/requirements.txt
```

## Configuração

### 1. Criar o arquivo `.env`

Crie um arquivo `.env` dentro da pasta `src/` com as seguintes variáveis:

```plaintext
GITHUB_CLIENT_ID="seu_client_id_aqui"
GITHUB_CLIENT_SECRET="seu_client_secret_aqui"
FERNET_KEY=""  # Opcional (será gerado automaticamente se não existir)
```

### 2. Configurar host (`src/auth.py` e `src/main.py`)

Caso se pretenda fazer deploy no Replit, é necessário alterar a URL e a porta para as fornecidas pelo servidor. Além disso, também é necessário atualizar as URLs na plataforma do servidor de autenticação.

`src/auth.py`:
```python
redirect_url='http://localhost:3000/oauth_callback',
# redirect_url='https://9add73eb-1d78-4beb-99c1-ddcc8e613ebd-00-2c518dp4o8er8.riker.replit.dev:3000/oauth_callback', # Replit
```

`src/main.py`:
```python
ft.app(main, port=8550, view=ft.AppView.WEB_BROWSER, host="localhost", assets_dir="src/assets")
# ft.app(main, port=3000, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", assets_dir="src/assets") # Replit
```

## Executando a Aplicação

Para iniciar a aplicação, utilize o seguinte comando no terminal:

```sh
python src/main.py
```

A aplicação estará disponível no navegador na URL correspondente à configuração do host e porta definidos no arquivo `src/main.py`.
