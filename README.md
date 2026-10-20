# RPA de Vagas LinkedIn com Python

Automação desenvolvida em Python para consultar alertas de vagas do LinkedIn recebidos por e-mail, extrair informações relevantes e consolidar os resultados em uma planilha Excel.

## Tecnologias utilizadas

- Python
- Gmail API
- Google OAuth 2.0
- BeautifulSoup4
- OpenPyXL

## Funcionalidades

- Autenticação segura na API do Gmail utilizando OAuth 2.0.
- Consulta de alertas de vagas do LinkedIn recebidos nos últimos 30 dias.
- Extração do identificador, cargo, empresa, modalidade e localização das vagas.
- Identificação e remoção de vagas duplicadas pelo ID.
- Geração de planilha Excel com filtros, cabeçalhos formatados e links clicáveis.
- Consolidação das vagas em uma única execução.

## Estrutura do projeto

```text
rpa_vagas_linkedin/
├── autenticacao.py
├── buscar_vagas.py
├── extrair_vagas.py
├── exportar_excel.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Instalação

Clone o repositório e acesse a pasta do projeto.

Crie um ambiente virtual:

```powershell
python -m venv .venv
```

Ative o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Instale as dependências:

```powershell
python -m pip install -r requirements.txt
```

## Configuração da API do Gmail

1. Crie um projeto no Google Cloud Console.
2. Ative a Gmail API.
3. Configure a tela de consentimento OAuth.
4. Crie credenciais OAuth 2.0 para aplicativo desktop.
5. Salve o arquivo JSON de credenciais na pasta do projeto com o nome `client_secret_key_apps_googleusercontent.json`.
6. Configure o usuário de teste, caso o aplicativo esteja em modo de testes.

Na primeira execução, será solicitada autorização de leitura dos e-mails. As credenciais autorizadas serão armazenadas localmente em `token.json`.

**Importante:** os arquivos de credenciais e tokens não devem ser publicados no GitHub.

## Execução

Para gerar a planilha de vagas:

```powershell
python exportar_excel.py
```

O programa consulta os alertas, extrai as vagas, elimina duplicidades e gera o arquivo `vagas_linkedin.xlsx`.

## Resultado

Durante os testes de desenvolvimento, o projeto consolidou 61 vagas únicas a partir dos alertas consultados.

A quantidade de vagas pode variar conforme os e-mails disponíveis na conta Gmail.

## Limitações e melhorias futuras

- A extração depende da estrutura HTML dos alertas do LinkedIn.
- A modalidade pode aparecer como "Não informada" quando não estiver explícita no alerta.
- Implementar filtros por tecnologias e perfil profissional.
- Preservar o histórico das vagas entre execuções.
- Implementar execução automática diária e gerenciamento adequado da autenticação OAuth.

## Segurança

O projeto utiliza acesso somente de leitura ao Gmail. Arquivos de credenciais, tokens e dados locais são excluídos do versionamento por meio do `.gitignore`.
