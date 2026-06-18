# 🎓 Certificados-IEEE

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![CustomTkinter](https://img.shields.io/badge/GUI-CustomTkinter-00A0D2)
![Pillow](https://img.shields.io/badge/Image-Pillow-238636)

Sistema interno de geração e distribuição automatizada de certificados para eventos do IEEE Student Branch UFC. A partir de uma planilha de participantes e de um template de imagem, o sistema produz arquivos PDF individuais com o nome de cada participante inserido e renderizado com precisão tipográfica matemática, e os distribui por e-mail via protocolo SMTP autenticado.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Manual de Configuração](#manual-de-configuração)
  - [1. Gerando a Senha de App no Google](#1-gerando-a-senha-de-app-no-google)
  - [2. Formatando a planilha de participantes](#2-formatando-a-planilha-de-participantes)
  - [3. Configurando o layout do certificado](#3-configurando-o-layout-do-certificado)
- [Operação da Interface](#operação-da-interface)
- [Modo Terminal](#modo-terminal)
- [Saída do Sistema](#saída-do-sistema)
- [Tratamento de Erros](#tratamento-de-erros)
- [Referência dos Módulos](#referência-dos-módulos)
- [Contribuição](#contribuição)

---

## Visão Geral

O sistema foi desenvolvido de forma modular para isolar atividades: leitura de dados, renderização de imagem, exportação em PDF e envio de e-mail são tratados por módulos independentes, todos acionados em sequência por um único arquivo central (`main.py`). Uma interface gráfica construída com CustomTkinter oferece uma execução segura e intuitiva, com log em tempo real e injeção de credenciais diretamente na memória RAM (eliminando arquivos estáticos vulneráveis).

**Funcionalidades principais:**

- Leitura higienizada de participantes a partir de arquivo CSV.
- Tipografia responsiva: cálculo de *Cap Height* e redução dinâmica para nomes muito longos.
- Geração de certificados em PDF centralizados matematicamente por *bounding box*.
- Envio automático de e-mail com o certificado em anexo (Gmail SMTP com autenticação via Senha de App).
- Interface gráfica com tema visual IEEE e barra de progresso alimentada por Threading.
- Validação de pré-requisitos antes do início da execução (arquivos, planilha e pesos).
- Registro de falhas de envio em arquivo de log sem interrupção do processo principal.

---

## Arquitetura do Sistema

~~~text
Certificados-IEEE/
├── app_gui.py                   # Ponto de entrada da interface gráfica
├── app_gui.spec                 # Regras de compilação para o PyInstaller
├── config.json                  # Parâmetros estruturais persistidos do layout
├── gerar_executavel.bat         # Script de automação para compilar a versão .exe
├── requirements.txt             # Dependências Python
│
├── assets/
│   ├── fontes/
│   │   └── Montserrat-Light.ttf # Fonte utilizada na renderização
│   └── templates/
│       ├── certificado.png      # Imagem base do certificado
│       └── logo_ieee.png        # Logo manipulada via canal Alpha na UI
│
├── data/
│   └── dados_teste.csv          # Planilha de exemplo para testes
│
└── src/
    ├── main.py                  # Orquestrador principal
    ├── leitor_csv.py            # Leitura e sanitização da planilha de participantes
    ├── motor_imagem.py          # Renderização tipográfica e dimensionamento
    ├── exportador.py            # Conversão RGB e salvamento em PDF
    ├── envio_email.py           # Estruturação MIME e disparo com rate-limiting
    ├── validador.py             # Verificação de pré-requisitos lógicos e físicos
    └── config_manager.py        # Gerenciador de I/O de preferências
~~~

**Fluxo de execução:**

~~~text
app_gui.py (Thread UI)
 │
 └─ config_manager.py (Persiste caminhos no JSON e injeta senhas na memória)
     │
     └─ main.py (Thread de Background)
         ├─ validador.py        Verifica arquivos físicos e integridade de bytes da planilha
         ├─ leitor_csv.py       Carrega a lista higienizada de dicionários
         ├─ motor_imagem.py     Calcula escala e desenha o texto ancorado
         ├─ exportador.py       Converte imagem para PDF (Drop RGBA) e salva em disco
         └─ envio_email.py      Codifica Base64 em UTF-8 e realiza disparo SMTP seguro
~~~

---

## Requisitos

| Componente | Versão mínima |
|---|---|
| Python | 3.10 |
| Sistema operacional | Windows 10, macOS 12, Ubuntu 20.04 |
| Conta Gmail | Com autenticação de dois fatores ativa |

**Dependências Python** (declaradas em `requirements.txt`):

| Pacote | Finalidade |
|---|---|
| `pandas` | Manipulação de dados tabulares avançada |
| `Pillow` | Processamento de imagem, tipografia e exportação PDF |
| `openpyxl` | Suporte a leitura nativa de planilhas `.xlsx` |
| `customtkinter` | Interface gráfica responsiva e moderna |

---

## Instalação

**1. Clone o repositório:**

~~~bash
git clone https://github.com/seu-usuario/Certificados-IEEE.git
cd Certificados-IEEE
~~~

**2. Crie e ative um ambiente virtual** (recomendado):

~~~bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
~~~

**3. Instale as dependências:**

~~~bash
pip install -r requirements.txt
~~~

**4. Verifique a instalação:**

~~~bash
python -c "import PIL, pandas, customtkinter; print('Ambiente OK')"
~~~

A saída esperada é `Ambiente OK`. Qualquer `ModuleNotFoundError` indica que o passo 3 não foi concluído.

---

## Manual de Configuração

### 1. Gerando a Senha de App no Google

O sistema autentica no Gmail via SMTP com TLS na porta 587. O Gmail não aceita a sua senha pessoal convencional para este acesso — é necessário gerar uma **Senha de App**, uma credencial de 16 caracteres.

**Pré-requisito:** a conta Gmail utilizada deve ter a Verificação em duas etapas ativa. Sem ela, a opção não existe.

1. Acesse [myaccount.google.com](https://myaccount.google.com) com a conta remetente.
2. Na aba **Segurança**, localize "Verificação em duas etapas" e garanta que está "Ativada".
3. Acesse a página de [Senhas de App](https://myaccount.google.com/apppasswords).
4. Crie um app chamado `Certificados IEEE UFC` e copie a senha de 16 dígitos gerada.
5. **Atenção:** Você usará essa senha diretamente na interface gráfica na hora de enviar os certificados.

---

### 2. Formatando a planilha de participantes

O sistema aceita nativamente arquivos `.csv` e `.xlsx`. 

**Estrutura obrigatória:**
A primeira linha deve conter as colunas obrigatórias **Nome** e **Email**. O sistema é tolerante a variações de maiúsculas/minúsculas (`NOME`, `nome`, etc). Outras colunas, como `Carga_Horaria`, podem existir, mas apenas Nome e Email serão processadas pelo motor base.

**Regras e restrições:**
- Linhas com campos de Nome ou Email vazios são sanitizadas e puladas automaticamente.
- O conteúdo do campo Nome nomeará o arquivo PDF. O sistema remove espaços desnecessários e caracteres inválidos (`/`, `\`, `:`, etc.) automaticamente.
- Para arquivos CSV: Salve como **CSV (separado por vírgulas)** e não "UTF-8 com BOM".

---

### 3. Configurando o layout do certificado

O layout e os insumos são atualizados automaticamente pela interface gráfica, mas são persistidos no arquivo `config.json` para agilizar execuções futuras.

**Como calibrar a coordenada vertical (Y):**
O sistema centraliza o texto horizontalmente de forma automática. Para definir a altura exata:
1. Abra seu template base em um editor de imagens (GIMP, Paint, Photoshop).
2. Posicione o mouse sobre a linha onde o nome deve assentar.
3. Leia a coordenada **Y** exibida na barra de status do software e insira este valor na interface gráfica.

---

## Operação da Interface

A interface gráfica é o modo principal e seguro para operação da ferramenta. Inicie com:

~~~bash
python src/app_gui.py
~~~

**1. Seleção de Insumos:**
Utilize os botões da interface para mapear a **Planilha**, o **Template** e a **Fonte** (.ttf ou .otf).

**2. Posicionamento:**
Insira o valor do eixo Y obtido na calibração (o padrão sugerido é 500).

**3. Autenticação Segura:**
Insira o E-mail Institucional e a Senha de App do Google. Estes dados ficam retidos apenas na memória RAM da aplicação e são destruídos ao fechar a janela.

**4. Execução e Logs:**
Ao clicar em **GERAR CERTIFICADOS**, a barra de progresso será ativada. O painel inferior exibe os logs em tempo real por esquema de cores:
* Azul claro (`INFO`): Processamento normal.
* Verde (`SUCESSO`): Lote concluído.
* Amarelo (`AVISO`): Situações contornáveis.
* Vermelho (`ERRO`): Falhas Críticas.

---

## Modo Terminal

Para execuções locais sem envio de e-mails (apenas renderização de PDFs para revisão), o motor pode ser acionado diretamente, lendo os últimos caminhos salvos no `config.json`:

~~~bash
cd src
python main.py
~~~
> *Nota: Como o terminal ignora a interface gráfica, ele não receberá as senhas de RAM e pulará automaticamente a etapa de envio SMTP, avisando no console: "[AVISO] Credenciais não fornecidas".*

---

## Saída do Sistema

Os PDFs são salvos dinamicamente na pasta `certificados_prontos/` junto ao diretório do executável. O padrão de nomenclatura substitui espaços por *underscores*:

| Nome na planilha | Arquivo gerado |
|---|---|
| `Ana Paula Souza` | `Certificado_Ana_Paula_Souza.pdf` |
| `Bruno Oliveira ` | `Certificado_Bruno_Oliveira.pdf` |

---

## Tratamento de Erros

A ferramenta conta com proteção nativa contra falhas em lote:

**1. Validação Fail-Fast (`validador.py`)**
Antes de alocar memória pesada para imagens, o sistema garante que:
* Os arquivos referenciados existem no disco.
* A planilha contém dados reais (barrando planilhas vazias menores que 15 bytes).

**2. Resiliência de Envio (`envio_email.py`)**
Se a conexão oscilar ou o e-mail de um discente for inválido, o motor captura a exceção, não derruba a aplicação, pula o erro, e grava silenciosamente as informações na raiz do projeto no arquivo `erros_envio.txt`.

Formato do log de resiliência:
~~~text
Falha ao enviar para Nome Completo (email@dominio.com) | Erro: <descrição técnica>
~~~

---

## Referência dos Módulos

### `src/leitor_csv.py`
**`carregar_dados_cvs(caminho_arquivo: str) -> List[Dict[str, str]]`**
Lê e sanitiza a planilha. Normaliza matematicamente os cabeçalhos para resolver *case-insensitivity* e retorna estruturas prontas.

### `src/motor_imagem.py`
**`carregar_assets(caminho_imagem: str, ...) -> Tuple[Image.Image, None]`**
Otimização de I/O que carrega o template pesado apenas uma vez na memória principal.

**`desenhar_nome_centralizado(imagem_copia: Image.Image, nome: str, ...) -> Image.Image`**
Implementa lógica de *Cap Height* com a string "A" para evitar distorção em fontes cursivas, e aplica loop restritivo para impedir que o texto ultrapasse 66% da largura.

### `src/exportador.py`
**`exportar_certificado(imagem: Image.Image, nome: str, ...) -> str`**
Converte forçosamente a matriz para RGB (descartando o canal Alpha de arquivos .png) para prevenir exceções na compilação do protocolo PDF.

### `src/envio_email.py`
**`disparar_email(lista_alunos: List[Dict[str, str]], ...) -> None`**
Orquestra o handshake TLS, encapsula os binários PDF em Base64, e injeta pausas randômicas (`time.sleep`) imitando comportamento humano para contornar limitadores de Spam.

### `src/config_manager.py`
**`salvar_config(novos_valores: Dict[str, Any]) -> None`**
Realiza *Merge* dinâmico para atualizar preferências de arquivo JSON sem deletar configurações legadas.

---

## Contribuição

Este é um projeto interno do **IEEE Student Branch UFC**. Para propor melhorias ou reportar problemas, abra uma _issue_ descrevendo o comportamento observado, os dados de entrada utilizados e os logs gerados na interface.

---
*Desenvolvido pelo Comitê de Projetos Técnicos do IEEE Student Branch UFC.*