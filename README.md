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