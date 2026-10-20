import base64
import re

from bs4 import BeautifulSoup
from autenticacao import autenticar_gmail


def extrair_html(partes):
    """Localiza e decodifica o conteúdo HTML do e-mail."""

    for parte in partes:
        if parte.get("mimeType") == "text/html":
            dados = parte.get("body", {}).get("data")

            if dados:
                return base64.urlsafe_b64decode(
                    dados
                ).decode("utf-8", errors="replace")

        html = extrair_html(parte.get("parts", []))

        if html:
            return html

    return None



def identificar_modalidade(descricao):
    """Identifica a modalidade de trabalho da vaga."""

    resultado = re.search(
        r"\((Remoto|Remota|Híbrido|Híbrida|Presencial)\)",
        descricao,
        re.IGNORECASE
    )

    if not resultado:
        return "Não informada"

    modalidade = resultado.group(1).lower()

    if modalidade in ("remoto", "remota"):
        return "Remoto"

    if modalidade in ("híbrido", "híbrida"):
        return "Híbrido"

    return "Presencial"



def identificar_cargo(descricao, empresa):
    """Extrai o cargo usando o nome da empresa."""

    if not empresa:
        return ""

    # A descrição normalmente separa empresa e local com " · ".
    parte_inicial = descricao.split(" · ", 1)[0]

    # Remove o nome da empresa somente quando aparece no final.
    if parte_inicial.endswith(empresa):
        cargo = parte_inicial[:-len(empresa)].strip()
        return cargo

    return ""


def identificar_localizacao(descricao):
    """Identifica a localização informada no alerta."""

    if " · " not in descricao:
        return "Não informada"

    # A localização aparece depois do separador.
    localizacao = descricao.split(" · ", 1)[1]

    # Remove a modalidade de trabalho.
    localizacao = re.sub(
        r"\s*\((Remoto|Remota|Híbrido|Híbrida|Presencial)\)",
        "",
        localizacao,
        flags=re.IGNORECASE
    )

    # Remove informações adicionais dos alertas.
    indicadores = [
        "Recrutando agora",
        "Crescimento rápido",
        "Candidatura simplificada",
        "ex-aluno",
        "ex-alunos",
        "ex-funcionário",
        "ex-funcionários",
        "conexão",
        "conexões",
        "R$"
    ]

    for indicador in indicadores:
        posicao = localizacao.find(indicador)

        if posicao != -1:
            localizacao = localizacao[:posicao]

    # Remove números associados a ex-funcionários,
    # ex-alunos e conexões do LinkedIn.
    localizacao = re.sub(
        r"\s+\d+\s*$",
        "",
        localizacao
    )

    localizacao = localizacao.strip()

    return localizacao if localizacao else "Não informada"


def extrair_vagas():
    """Consulta alertas e consolida vagas pelo ID."""

    gmail = autenticar_gmail()

    consulta = "from:jobalerts-noreply@linkedin.com newer_than:30d"

    resposta = gmail.users().messages().list(
        userId="me",
        q=consulta,
        maxResults=20
    ).execute()

    mensagens = resposta.get("messages", [])

    print(f"\nE-mails encontrados: {len(mensagens)}")

    vagas = {}

    for numero, mensagem in enumerate(mensagens, start=1):

        print(f"Processando e-mail {numero}/{len(mensagens)}...")

        email = gmail.users().messages().get(
            userId="me",
            id=mensagem["id"],
            format="full"
        ).execute()

        html = extrair_html([email["payload"]])

        if not html:
            continue

        soup = BeautifulSoup(html, "html.parser")

        for link in soup.find_all("a", href=True):
            texto = link.get_text(" ", strip=True)
            url = link["href"]

            resultado = re.search(r"/jobs/view/(\d+)", url)

            if not resultado:
                continue

            id_vaga = resultado.group(1)

            # Identifica o nome da empresa pelo logotipo.
            imagem = link.find("img", alt=True)
            empresa = imagem["alt"].strip() if imagem else ""

            url_vaga = (
                f"https://www.linkedin.com/jobs/view/{id_vaga}/"
            )


            # Cria o registro da vaga, caso ainda não exista.
            if id_vaga not in vagas:
                vagas[id_vaga] = {
                    "id": id_vaga,
                    "descricao": "",
                    "empresa": "",
                    "modalidade": "",
                    "cargo": "",
                    "localizacao": "",
                    "url": url_vaga
                }

            # Mantém a descrição mais completa.
            if len(texto) > len(vagas[id_vaga]["descricao"]):
                vagas[id_vaga]["descricao"] = texto

            vagas[id_vaga]["modalidade"] = identificar_modalidade(
                vagas[id_vaga]["descricao"]
            )

            # Guarda a empresa quando encontrada no logotipo.
            if empresa and not vagas[id_vaga]["empresa"]:
                vagas[id_vaga]["empresa"] = empresa

            vagas[id_vaga]["localizacao"] = identificar_localizacao(
             vagas[id_vaga]["descricao"]
            )

    for vaga in vagas.values():
        vaga["cargo"] = identificar_cargo(
            vaga["descricao"],
            vaga["empresa"]
        )

    print("\n" + "=" * 60)
    print("RESULTADO DA CONSOLIDAÇÃO")
    print("=" * 60)

    print(f"E-mails processados: {len(mensagens)}")
    print(f"Vagas únicas encontradas: {len(vagas)}")

    print("\nLISTA DE VAGAS:\n")

    for numero, vaga in enumerate(vagas.values(), start=1):
        print(f"Vaga {numero}")
        print(f"ID: {vaga['id']}")
        print(f"Empresa: {vaga['empresa']}")
        print(f"Modalidade: {vaga['modalidade']}")
        print(f"Cargo: {vaga['cargo']}")
        print(f"Localização: {vaga['localizacao']}")
        print(f"Descrição: {vaga['descricao']}")
        print(f"Link: {vaga['url']}")
        print("-" * 60)

    return vagas


if __name__ == "__main__":
    extrair_vagas()
