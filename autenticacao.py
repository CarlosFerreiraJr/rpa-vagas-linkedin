############################################################################
# Finalidade do Código
# Verifica se já existe um token.json. Caso exista, tenta reutilizá-lo
# ou renová-lo automaticamente. Caso contrário, abre o navegador para você
# autorizar o acesso ao Gmail.
#
# Depois, realiza uma consulta simples ao perfil da conta para confirmar
# a conexão.
############################################################################

from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


# Permissão somente para leitura dos e-mails.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Diretório do projeto.
BASE_DIR = Path(__file__).resolve().parent

# Arquivos de autenticação.
CREDENTIALS_FILE = BASE_DIR / "client_secret_key_apps_googleusercontent.json"
TOKEN_FILE = BASE_DIR / "token.json"


def autenticar_gmail():
    credenciais = None

    # Reutiliza o token salvo, caso exista.
    if TOKEN_FILE.exists():
        credenciais = Credentials.from_authorized_user_file(
            str(TOKEN_FILE), SCOPES
        )

    # Solicita ou renova a autorização quando necessário.
    if not credenciais or not credenciais.valid:

        if credenciais and credenciais.expired and credenciais.refresh_token:
            credenciais.refresh(Request())
        else:
            fluxo = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            credenciais = fluxo.run_local_server(port=0)

        # Salva as credenciais para as próximas execuções.
        TOKEN_FILE.write_text(
            credenciais.to_json(),
            encoding="utf-8"
        )

    # Cria o serviço da Gmail API.
    servico = build("gmail", "v1", credentials=credenciais)

    return servico


if __name__ == "__main__":
    gmail = autenticar_gmail()
    perfil = gmail.users().getProfile(userId="me").execute()

    print("Autenticação realizada com sucesso!")
    print(f"Gmail conectado: {perfil['emailAddress']}")
