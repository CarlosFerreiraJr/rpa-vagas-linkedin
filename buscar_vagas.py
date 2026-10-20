
from datetime import datetime
from autenticacao import autenticar_gmail


def buscar_alertas_linkedin():
    # Conecta à Gmail API usando nossa autenticação.
    gmail = autenticar_gmail()

    # Pesquisa mensagens recebidas do LinkedIn.
    consulta = "from:jobalerts-noreply@linkedin.com newer_than:30d"

    resposta = gmail.users().messages().list(
        userId="me",
        q=consulta,
        maxResults=20
    ).execute()

    mensagens = resposta.get("messages", [])

    if not mensagens:
        print("Nenhum e-mail do LinkedIn encontrado.")
        return

    print(f"Encontrados {len(mensagens)} e-mails.\n")

    for mensagem in mensagens:
        # Recupera os metadados da mensagem.
        email = gmail.users().messages().get(
            userId="me",
            id=mensagem["id"],
            format="metadata",
            metadataHeaders=["Subject", "Date", "From"]
        ).execute()

        cabecalhos = {
            item["name"].lower(): item["value"]
            for item in email["payload"]["headers"]
        }

        print(f"Assunto: {cabecalhos.get('subject', 'Sem assunto')}")
        print(f"Data: {cabecalhos.get('date', 'Sem data')}")
        print(f"Remetente: {cabecalhos.get('from', 'Desconhecido')}")
        print("-" * 60)


if __name__ == "__main__":
    buscar_alertas_linkedin()
