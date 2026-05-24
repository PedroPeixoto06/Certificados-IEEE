# Certificados-IEEE

Sistema interno de geração e distribuição automatizada de certificados para eventos do IEEE Student Branch UFC. A partir de uma planilha de participantes e de um template de imagem, o sistema produz arquivos PDF individuais com o nome de cada participante inserido e renderizado com precisão tipográfica, e os distribui por e-mail via protocolo SMTP autenticado.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Arquitetura do Sistema](#arquitetura-do-sistema)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Manual de Configuração](#manual-de-configuração)
  - [1. Gerando a Senha de App no Google](#1-gerando-a-senha-de-app-no-google)
  - [2. Configurando o arquivo .env](#2-configurando-o-arquivo-env)
  - [3. Formatando a planilha de participantes](#3-formatando-a-planilha-de-participantes)
  - [4. Configurando o layout do certificado](#4-configurando-o-layout-do-certificado)
- [Operação da Interface](#operação-da-interface)
- [Modo Terminal](#modo-terminal)
- [Saída do Sistema](#saída-do-sistema)
- [Tratamento de Erros](#tratamento-de-erros)
- [Referência dos Módulos](#referência-dos-módulos)
- [Contribuição](#contribuição)

---

## Visão Geral

O sistema foi desenvolvido de forma modular para isolar atividades: leitura de dados, renderização de imagem, exportação em PDF e envio de e-mail são tratados por módulos independentes, todos acionados em sequência por um único arquivo central (main.py). Uma interface gráfica construída com CustomTkinter oferece uma alternativa ao modo de execução por terminal, com log de execução em tempo real e validação antecipada de todos os pré-requisitos.

**Funcionalidades principais:**

- Leitura de participantes a partir de arquivo CSV
- Geração de certificados em PDF com nome centralizado dinamicamente sobre o template
- Envio automático de e-mail com o certificado em anexo (Gmail SMTP com autenticação via Senha de App)
- Interface gráfica com tema visual IEEE
- Validação de pré-requisitos antes do início da execução (credenciais, arquivos, planilha)
- Registro de falhas de envio em arquivo de log sem interrupção do processo principal

---

## Arquitetura do Sistema

```
Certificados-IEEE/
├── app_gui.py                   # Ponto de entrada da interface gráfica
├── config.json                  # Parâmetros de layout do certificado
├── requirements.txt             # Dependências Python
├── .env                         # Credenciais
│
├── assets/
│   ├── fontes/
│   │   └── Montserrat-Light.ttf # Fonte utilizada na renderização
│   └── templates/
│       └── certificado.png      # Imagem base do certificado
│
├── data/
│   └── dados_teste.csv          # Planilha de exemplo para testes
│
└── src/
    ├── main.py                  # Orquestrador principal
    ├── leitor_csv.py            # Leitura e interpretação da planilha de participantes
    ├── motor_imagem.py          # Renderização tipográfica sobre a imagem
    ├── exportador.py            # Conversão e salvamento em PDF
    ├── envio_email.py           # Estruturaçao e disparo de e-mails
    ├── validador.py             # Verificação de pré-requisitos
    └── testeconexao.py          # Diagnóstico da conexão SMTP
```

**Fluxo de execução:**

```
main.py
  │
  ├─ validador.py        Verifica .env, arquivos e integridade da planilha
  ├─ leitor_csv.py       Carrega a lista de participantes como dicionários
  ├─ motor_imagem.py     Abre o template e desenha o nome centrado por bounding box
  ├─ exportador.py       Converte a imagem renderizada para PDF e salva em disco
  └─ envio_email.py      Monta o e-mail HTML, anexa o PDF e realiza o disparo SMTP
```

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
| `pandas` | Manipulação de dados tabulares |
| `Pillow` | Processamento de imagem e exportação PDF |
| `openpyxl` | Suporte a planilhas `.xlsx` |
| `python-dotenv` | Carregamento de variáveis de ambiente |
| `customtkinter` | Interface gráfica moderna (instalação separada) |

---

## Instalação

**1. Clone o repositório:**

```bash
git clone https://github.com/seu-usuario/Certificados-IEEE.git
cd Certificados-IEEE
```

**2. Crie e ative um ambiente virtual** (recomendado):

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Instale as dependências:**

```bash
pip install -r requirements.txt
pip install customtkinter
```

**4. Verifique a instalação:**

```bash
python -c "import PIL, pandas, customtkinter, dotenv; print('Ambiente OK')"
```

A saída esperada é `Ambiente OK`. Qualquer `ModuleNotFoundError` indica que o passo 3 não foi concluído corretamente.

---

## Manual de Configuração

Esta seção descreve os passos obrigatórios antes da primeira execução: geração da Senha de App no Google, configuração do arquivo `.env`, preparação da planilha de participantes e ajuste do layout do certificado.

---

### 1. Gerando a Senha de App no Google

O sistema autentica no Gmail via SMTP com TLS na porta 587. O Gmail não aceita a senha convencional da conta para esse tipo de acesso — é necessário gerar uma **Senha de App**, uma credencial de 16 caracteres criada especificamente para aplicações externas.

**Pré-requisito:** a conta Gmail utilizada deve ter a Verificação em duas etapas ativa. Sem ela, a opção de Senha de App não é exibida.

---

**Passo 1 — Acesse as configurações de segurança da conta**

Acesse [myaccount.google.com](https://myaccount.google.com) com a conta que será usada como remetente. No menu lateral, clique em "Segurança". Localize a seção "Como você faz login no Google". O item "Verificação em duas etapas" deve exibir o status "Ativada". 

---

**Passo 2 — Acesse a página de Senhas de App**

Com a verificação em duas etapas ativa, acesse https://myaccount.google.com/apppasswords


---

**Passo 3 — Crie a Senha de App**

No campo "Nome do app", insira um nome descritivo para identificar essa credencial, por exemplo: `Certificados IEEE UFC`. Clique em "Criar".

---

**Passo 4 — Copie a senha gerada**

Uma janela exibirá a senha — uma sequência de 16 caracteres no formato `xxxx xxxx xxxx xxxx`. Copie a senha neste momento. Ela não poderá ser visualizada novamente após fechar esta janela. Os espaços entre os grupos de quatro caracteres podem ser removidos ou mantidos ao colar no `.env` — ambos os formatos são aceitos pelo servidor SMTP.

Copie a senha e feche o modal clicando em "Concluir".

> **Nota de segurança:** Cada Senha de App é exclusiva para o par conta/aplicação. Se a senha for comprometida ou perdida, revogue-a nessa mesma página e gere uma nova. A revogação não afeta o acesso normal à conta Google nem outras Senhas de App existentes.

---

### 2. Configurando o arquivo .env

O arquivo `.env` isola as credenciais do código-fonte. Ele deve ser criado manualmente na raiz do projeto, na mesma pasta onde estão `app_gui.py` e `config.json`.

**Passo 1 — Crie o arquivo**

No Windows (via terminal):

```cmd
type nul > .env
```

No macOS/Linux:

```bash
touch .env
```

> **Atencao para usuários Windows:** o Explorador de Arquivos pode exibir o arquivo como `.env.txt` se as extensões conhecidas estiverem ocultas. Use o terminal para criar e editar o arquivo para garantir o nome correto.

**Passo 2 — Edite o arquivo**

Abra `.env` em qualquer editor de texto (VS Code, Notepad++, nano) e insira:

```
email_user = seuemail@gmail.com
senha_user = suasenhadedezesseis
```

Substitua `seuemail@gmail.com` pelo endereço Gmail completo do remetente e `suasenhadedezesseis` pela Senha de App gerada no passo anterior (sem espaços).

**Passo 3 — Valide a configuração**

Execute o script de diagnóstico para confirmar que as credenciais estão corretas:

```bash
cd src
python testeconexao.py
```

Saída esperada:

```
Tentando conectar com: seuemail@gmail.com...
[SUCESSO] Conexão e login realizados com sucesso!
```

Caso ocorra falha, consulte a tabela de erros comuns:

| Mensagem de erro | Causa provável |
|---|---|
| `Username and Password not accepted` | Senha de App incorreta ou copiada com espaços extras |
| `Please log in via your web browser` | Conta sem verificação em duas etapas ativa |
| `getaddrinfo failed` | Sem conexão com a internet |
| `Connection refused` | Porta 587 bloqueada pela rede local (comum em redes corporativas e universitárias) |

> **Importante:** O arquivo `.env` já está declarado no `.gitignore` e nunca será incluído em commits automaticamente. Não o adicione manualmente ao controle de versão nem o compartilhe por outros canais.

---

### 3. Formatando a planilha de participantes

O sistema aceita planilhas nos formatos `.csv` e `.xlsx`. O arquivo `data/dados_teste.csv` pode ser usado como modelo de referência.

**Estrutura obrigatória:**

A primeira linha deve conter exatamente os seguintes cabeçalhos:

| Coluna | Tipo | Descrição |
|---|---|---|
| `Nome` | Texto | Nome completo do participante, exatamente como deve aparecer no certificado |
| `Email` | Texto | Endereço de e-mail para envio do certificado |
| `Carga_Horaria` | Número inteiro | Carga horária de participação no evento |

**Exemplo de arquivo válido:**

```
Nome,Email,Carga_Horaria
Ana Souza,anasouza@email.com,40
Bruno Costa,brunocosta@email.com,32
Carla Mendes,carlamendes@email.com,40
```

**Regras e restrições:**

- Os cabeçalhos são sensíveis a maiúsculas e minúsculas. `nome`, `NOME` ou `Nome ` (com espaço) causarão falha silenciosa na leitura dos dados.
- Linhas com os campos `Nome` ou `Email` vazios são ignoradas pelo sistema.
- Espaços extras no início ou fim dos valores são removidos automaticamente.
- O conteúdo do campo `Nome` é usado diretamente no certificado gerado e no nome do arquivo PDF. Evite caracteres como `/`, `\`, `:`, `*`, `?`, `"`, `<`, `>` e `|`, que são inválidos em nomes de arquivo em sistemas Windows.
- O encoding esperado pelo leitor é `latin-1`. Ao salvar como CSV pelo Microsoft Excel, selecione **CSV (separado por vírgulas)** — não a variante "UTF-8 com BOM", que pode causar problema na leitura do cabeçalho.
- Não inclua linhas completamente vazias entre os registros.

**Salvando como CSV:**

- **Microsoft Excel:** `Arquivo > Salvar como > Tipo: CSV (separado por vírgulas) (*.csv)`
- **Google Sheets:** `Arquivo > Fazer download > Valores separados por vírgula (.csv)`

Após salvar, mova o arquivo para a pasta `data/` ou atualize o campo `planilha_dados` no `config.json` com o caminho correspondente.

---

### 4. Configurando o layout do certificado

O arquivo `config.json` centraliza todos os parâmetros de posicionamento e estilo. Nenhuma alteração no código-fonte é necessária para ajustar o layout.

```json
{
    "configuracoes_certificado": {
        "arquivos": {
            "imagem_base": "assets/templates/certificado.png",
            "fonte_nome": "assets/fontes/Montserrat-Light.ttf",
            "planilha_dados": "data/dados_teste.csv"
        },
        "fonte": {
            "tamanho": 40,
            "cor": "#000000"
        },
        "posicao_nome": {
            "x": 800,
            "y": 495,
            "alinhamento": "centro"
        }
    }
}
```

**Referência de parâmetros:**

| Chave | Tipo | Descrição |
|---|---|---|
| `arquivos.imagem_base` | String (caminho relativo) | Template do certificado. Formatos aceitos: `.png`, `.jpg`, `.jpeg`. Recomenda-se `.png` para preservar qualidade na saída PDF. |
| `arquivos.fonte_nome` | String (caminho relativo) | Arquivo de fonte TrueType (`.ttf`). A fonte é lida diretamente do arquivo — não depende de fontes instaladas no sistema operacional. |
| `arquivos.planilha_dados` | String (caminho relativo) | Arquivo CSV ou XLSX com os participantes. |
| `arquivos.pasta_saida` | String (caminho relativo) | (Opcional) Pasta de destino dos PDFs gerados. Padrão: `certificados_prontos`. Criada automaticamente se não existir. |
| `fonte.tamanho` | Inteiro | Tamanho da fonte em pontos tipográficos. |
| `fonte.cor` | String (hexadecimal) | Cor do texto. Exemplos: `"#000000"` (preto), `"#FFFFFF"` (branco). |
| `posicao_nome.y` | Inteiro | Posição vertical do nome em pixels, medida a partir do topo da imagem. |

> **Nota sobre centralização horizontal:** o módulo `motor_imagem.py` centraliza o nome automaticamente usando o bounding box do texto em relação à largura total da imagem. O parâmetro `posicao_nome.x` presente no arquivo de configuração é lido mas não utilizado na renderização atual.

**Como calibrar o valor de `posicao_nome.y`:**

Abra o arquivo de template em um editor de imagem (GIMP, Photoshop, Paint.NET). Posicione o cursor sobre a linha onde os nomes devem ser escritos. A coordenada Y exibida na barra de status do editor corresponde ao valor a ser inserido em `posicao_nome.y`.

---

## Operação da Interface

A interface gráfica é o modo de uso recomendado para operadores sem familiaridade com o terminal.

**Iniciando a aplicação:**

```bash
python app_gui.py
```

**Área de seleção de arquivos**

A janela principal apresenta dois seletores de arquivo:

- **Planilha de Participantes:** aceita `.csv`, `.xlsx` e `.xls`. Ao clicar em "Selecionar", uma janela do sistema operacional é aberta para navegar até o arquivo.
- **Template do Certificado:** aceita `.png`, `.jpg` e `.jpeg`.

Após a seleção, o caminho completo do arquivo é exibido abaixo do respectivo seletor.


**Executando a geração**

Com os dois arquivos selecionados, clique em **GERAR CERTIFICADOS**. O botão é desabilitado durante o processamento para evitar execuções concorrentes. Uma barra de progresso indeterminada é exibida abaixo do botão enquanto o processo ocorre em thread separada, mantendo a interface responsiva.

**Lendo o log de execução**

O painel inferior exibe mensagens em tempo real. As cores indicam o tipo de cada mensagem:

| Cor | Tipo | Significado |
|---|---|---|
| Azul claro | INFO | Progresso normal da execução |
| Verde | SUCESSO | Etapa concluída com êxito |
| Amarelo | AVISO | Situação que requer atenção mas não interrompe a execução |
| Vermelho | ERRO | Falha em uma etapa específica |


**Interpretando o resultado:**

- `Processo finalizado com sucesso!` — todos os certificados foram gerados e os e-mails foram disparados. Falhas individuais de envio, se houver, estão registradas em `erros_envio.txt`.
- `Processo encerrado com erros.` — uma falha crítica interrompeu a execução. Localize a linha vermelha no log para identificar a causa e consulte a seção [Tratamento de Erros](#tratamento-de-erros).

---

## Modo Terminal

O modo terminal executa o mesmo pipeline da interface gráfica, lendo os parâmetros diretamente do `config.json`.

```bash
cd src
python main.py
```

**Saída esperada em execução normal:**

```
--- INICIANDO MOTOR DE CERTIFICADOS IEEE ---
[VALIDACAO] Checando pré-requisitos do sistema...
[OK] Todos os pré-requisitos foram validados com sucesso.

[INFO] Parâmetros lidos com sucesso:
 -> Imagem Base: /caminho/assets/templates/certificado.png
 -> Fonte Oficial: /caminho/assets/fontes/Montserrat-Light.ttf
 -> Coordenadas de Injeção: X=800, Y=495
 -> Planilha Alvo: /caminho/data/dados_teste.csv

 [DADOS] Lendo: data/dados_teste.csv
[ASSETS] Carregando imagem e fonte...

[STATUS] Processando N certificados...
[OK] Certificado gerado: /caminho/certificados_prontos/Certificado_Nome.pdf
...

==================================================
[SUCESSO] CONCLUIDO EM X.XX segundos
[DIRETORIO] CERTIFICADOS EM: /caminho/certificados_prontos
==================================================

[TRANSIÇÃO] Iniciando o envio de e-mails para os alunos...
[ENVIADO] E-mail entregue com sucesso para email@dominio.com
...
[SUCESSO] Linha de disparo finalizada.
```

---

## Saída do Sistema

Os PDFs são salvos em `certificados_prontos/` (ou no caminho definido em `config.json` via `pasta_saida`) com o seguinte padrão de nomenclatura:

```
Certificado_Nome_Do_Participante.pdf
```

Espaços no nome são substituídos por underscores. Espaços extras no início ou fim do nome são removidos antes da substituição.

**Exemplos:**

| Nome na planilha | Arquivo gerado |
|---|---|
| `Ana Paula Souza` | `Certificado_Ana_Paula_Souza.pdf` |
| `Bruno Oliveira ` | `Certificado_Bruno_Oliveira.pdf` |

---

## Tratamento de Erros

O sistema implementa dois níveis de proteção contra falhas:

**Validação antecipada (`validador.py`)**

Antes de qualquer processamento, o validador verifica sequencialmente:

1. Existência e leitura das chaves `email_user` e `senha_user` no `.env`
2. Existência do arquivo de fonte no caminho configurado
3. Existência do arquivo de imagem base no caminho configurado
4. Existência e tamanho mínimo da planilha (arquivos com menos de 15 bytes são tratados como vazios)

Se qualquer verificação falhar, a execução é encerrada com uma mensagem descritiva antes de qualquer tentativa de leitura de imagem ou envio de e-mail.

**Resiliência no envio (`envio_email.py`)**

Falhas no envio para um participante específico são capturadas individualmente. O erro é registrado em `erros_envio.txt` com nome, e-mail e descrição, e o processo avança para o próximo participante.

Formato do log de erros:

```
Falha ao enviar para Nome Completo (email@dominio.com) | Erro: <descrição>
```

---

## Referência dos Módulos

### `src/leitor_csv.py`

**`carregar_dados_cvs(caminho_arquivo: str) -> list[dict]`**

Lê um arquivo CSV e retorna uma lista de dicionários com as chaves `nome` e `email`. Linhas com campos ausentes são ignoradas. Encoding esperado: `latin-1`.

---

### `src/motor_imagem.py`

**`carregar_assets(caminho_imagem, caminho_fonte, tamanho_fonte) -> tuple[Image, ImageFont]`**

Abre a imagem base e a fonte TrueType uma única vez, retornando os objetos para reutilização no loop de geração. Operação de I/O realizada fora do loop para ganho de desempenho.

**`desenhar_nome_centralizado(imagem_copia, nome, fonte, altura_y_fixa) -> Image`**

Recebe uma cópia isolada da imagem base e desenha o nome centralizado horizontalmente via cálculo de bounding box. Retorna a imagem modificada.

---

### `src/exportador.py`

**`exportar_certificado(imagem, nome, pasta_saida) -> str`**

Converte a imagem PIL para RGB (requisito do Pillow para exportação PDF), salva em disco com resolução de 150 DPI e retorna o caminho completo do arquivo. Cria a pasta de saída se não existir.

---

### `src/envio_email.py`

**`disparar_email(lista_alunos: list[dict], pasta_certificados: str) -> None`**

Estabelece uma única conexão SMTP com o Gmail, itera pela lista de participantes, monta o e-mail HTML com o PDF em anexo e realiza o envio. Aplica pausa aleatória entre 3 e 6 segundos entre envios para reduzir risco de bloqueio por volume. Encerra a conexão ao término do loop.

---

### `src/validador.py`

**`validar_insumos(config: dict, diretorio_raiz: str) -> tuple[bool, str]`**

Retorna `(True, mensagem_ok)` se todos os pré-requisitos estiverem satisfeitos, ou `(False, mensagem_de_erro)` na primeira falha encontrada. Deve ser invocado antes de qualquer operação de I/O.

---

### `src/testeconexao.py`

Script de diagnóstico autônomo. Lê as credenciais do `.env`, tenta estabelecer conexão SMTP com o Gmail e imprime o resultado. Execute com `python testeconexao.py` para verificar a configuração antes do primeiro uso.

---

## Contribuição

Este é um projeto interno do **IEEE Student Branch UFC**. Para propor melhorias ou reportar problemas, abra uma _issue_ descrevendo o comportamento observado e o comportamento esperado.

---

*IEEE Student Branch UFC — Sistema interno de emissão de certificados*