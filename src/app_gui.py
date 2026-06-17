import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import os
import sys
from typing import List, Tuple, Any

# ── RESOLUÇÃO DINÂMICA DE DIRETÓRIOS ──
# Garante compatibilidade de rotas tanto no ambiente de desenvolvimento (VS Code)
# quanto no ambiente de produção (executável empacotado pelo PyInstaller).
if getattr(sys, 'frozen', False):
    DIRETORIO_RAIZ = sys._MEIPASS
    DIRETORIO_EXECUTAVEL = os.path.dirname(sys.executable)
    SRC_PATH = os.path.join(sys._MEIPASS, "src")
else:
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    DIRETORIO_RAIZ = os.path.dirname(DIRETORIO_ATUAL)
    DIRETORIO_EXECUTAVEL = DIRETORIO_RAIZ
    SRC_PATH = DIRETORIO_ATUAL

if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# ── TEMA E APARÊNCIA GLOBAL ──
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ── PALETA DE CORES INSTITUCIONAL (IEEE) ──
COR_FUNDO        = "#0D1117"   
COR_PAINEL       = "#161B22"   
COR_BORDA        = "#1F2937"   
COR_IEEE_AZUL    = "#006699"   
COR_IEEE_CLARO   = "#00A0D2"   
COR_TEXTO        = "#E6EDF3"   
COR_SUBTEXTO     = "#8B949E"   
COR_SUCESSO      = "#238636"   
COR_AVISO        = "#E3B341"   
COR_ERRO         = "#DA3633"   
COR_BOTAO_GERAR  = "#0D6EFD"   
COR_BOTAO_HOVER  = "#0B5ED7"


class LogBox(ctk.CTkFrame):
    """
    Componente visual personalizado para exibição de logs do sistema.
    Implementa barra de rolagem automática e coloração condicional de texto.
    """

    def __init__(self, master: Any, **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=COR_PAINEL, corner_radius=10,
                       border_width=1, border_color=COR_BORDA)

        self._text = tk.Text(
            self,
            bg=COR_PAINEL,
            fg=COR_TEXTO,
            font=("Courier New", 11),
            bd=0,
            highlightthickness=0,
            wrap="word",
            state="disabled",
            padx=12,
            pady=10,
        )
        scrollbar = ctk.CTkScrollbar(self, command=self._text.yview)
        self._text.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y", padx=(0, 4), pady=4)
        self._text.pack(side="left", fill="both", expand=True)

        # Mapeamento de tags para coloração sintática dos logs
        self._text.tag_config("INFO",    foreground=COR_IEEE_CLARO)
        self._text.tag_config("SUCESSO", foreground=COR_SUCESSO)
        self._text.tag_config("ERRO",    foreground=COR_ERRO)
        self._text.tag_config("AVISO",   foreground=COR_AVISO)
        self._text.tag_config("NORMAL",  foreground=COR_TEXTO)

    def append(self, msg: str, tipo: str = "NORMAL") -> None:
        """
        Insere uma nova linha de registro no painel de log e rola a tela para o final.
        
        Args:
            msg (str): O conteúdo da mensagem a ser exibida.
            tipo (str): Categoria do log (INFO, SUCESSO, ERRO, AVISO, NORMAL) que define a cor.
        """
        self._text.configure(state="normal")
        self._text.insert("end", msg + "\n", tipo)
        self._text.see("end")
        self._text.configure(state="disabled")

    def limpar(self) -> None:
        """Apaga todo o conteúdo atual do painel de logs."""
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")


class FileSelector(ctk.CTkFrame):
    """
    Componente visual modular para seleção de arquivos.
    Agrupa ícone, descritivo, exibição de caminho e botão de ação em uma única linha responsiva.
    """

    def __init__(self, master: Any, label: str, icone: str, tipos: List[Tuple[str, str]], **kwargs) -> None:
        super().__init__(master, **kwargs)
        self.configure(fg_color=COR_PAINEL, corner_radius=10,
                       border_width=1, border_color=COR_BORDA)
        
        self._tipos = tipos
        self._caminho = tk.StringVar(value="Nenhum arquivo selecionado")

        ctk.CTkLabel(self, text=icone, font=("Segoe UI Emoji", 22),
                     fg_color="transparent", text_color=COR_IEEE_CLARO,
                     width=40).pack(side="left", padx=(14, 4), pady=12)

        bloco = ctk.CTkFrame(self, fg_color="transparent")
        bloco.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(bloco, text=label, font=("Segoe UI", 13, "bold"),
                     text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(bloco, textvariable=self._caminho,
                     font=("Courier New", 10),
                     text_color=COR_SUBTEXTO, anchor="w",
                     wraplength=340).pack(anchor="w")

        self._btn = ctk.CTkButton(
            self, text="Selecionar",
            width=110, height=36,
            fg_color=COR_IEEE_AZUL, hover_color=COR_IEEE_CLARO,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8,
            command=self._selecionar,
        )
        self._btn.pack(side="right", padx=14, pady=12)

    def _selecionar(self) -> None:
        """Abre a caixa de diálogo nativa do sistema operacional para seleção de arquivo."""
        caminho = filedialog.askopenfilename(filetypes=self._tipos)
        if caminho:
            self._caminho.set(caminho)

    @property
    def caminho(self) -> str:
        """Retorna o caminho absoluto do arquivo selecionado ou string vazia se nada for escolhido."""
        val = self._caminho.get()
        return "" if val == "Nenhum arquivo selecionado" else val

    def resetar(self) -> None:
        """Restaura o componente para o estado inicial sem seleção."""
        self._caminho.set("Nenhum arquivo selecionado")


class App(ctk.CTk):
    """
    Janela principal da aplicação. 
    Gerencia o ciclo de vida da interface gráfica, a injeção de dependências e a 
    orquestração assíncrona (Threads) para o motor de processamento em lote.
    """
    def __init__(self) -> None:
        super().__init__()
        self.title("IEEE — Gerador de Certificados")
        self.geometry("640x780")
        self.minsize(580, 700)
        self.configure(fg_color=COR_FUNDO)
        self.resizable(True, True)

        self._build_ui()
    # ──────────────────────────────────────────────
    #  CONSTRUÇÃO DA INTERFACE
    # ──────────────────────────────────────────────
    def _build_ui(self) -> None:
        """
        Monta a árvore de componentes visuais da aplicação.
        Estrutura o cabeçalho dinâmico (com tratamento de transparência do logotipo),
        os formulários de entrada de dados, barras de progresso e painel de log.
        """
        # ── Cabeçalho ──
        header = ctk.CTkFrame(self, fg_color=COR_PAINEL, corner_radius=0, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(expand=True)

        # ── Instanciação e Tratamento do Logotipo ──
        logo_path = os.path.join(DIRETORIO_RAIZ, "assets", "logo_ieee.png")
        if os.path.exists(logo_path):
            pil_logo = Image.open(logo_path)
            
            # Conversão explícita para RGBA para manipulação do canal de transparência
            pil_logo = pil_logo.convert('RGBA')
            
            # Extração de fundo branco sólido via manipulação direta da matriz de pixels
            datas = pil_logo.getdata()
            newData = []
            for item in datas:
                # Tolerância para remoção de pixels excessivamente claros (brancos)
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    newData.append((255, 255, 255, 0)) # Converte para pixel transparente
                else:
                    newData.append(item)
            
            pil_logo.putdata(newData)
                
            # Dimensionamento proporcional baseado em uma altura fixa para não deformar a imagem
            altura_fixa = 60
            largura_orig, altura_orig = pil_logo.size
            proporcao = largura_orig / altura_orig
            largura_calc = int(proporcao * altura_fixa)
            
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(largura_calc, altura_fixa))
            
            logo_label = ctk.CTkLabel(logo_frame, image=ctk_logo, text="", fg_color="transparent")
            logo_label.pack(side="left", padx=(0, 12))
        else:
            ctk.CTkLabel(
                logo_frame,
                text="⬡ IEEE",
                font=("Georgia", 32, "bold"),
                text_color=COR_IEEE_CLARO,
            ).pack(side="left", padx=(0, 12))

        ctk.CTkFrame(logo_frame, fg_color=COR_BORDA, width=2, height=50).pack(side="left", padx=8)

        subtitulo = ctk.CTkFrame(logo_frame, fg_color="transparent")
        subtitulo.pack(side="left")
        ctk.CTkLabel(subtitulo, text="Gerador de Certificados", font=("Segoe UI", 16, "bold"), text_color=COR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(subtitulo, text="Instituto de Engenheiros Eletricistas e Eletrônicos", font=("Segoe UI", 10), text_color=COR_SUBTEXTO).pack(anchor="w")

        # ── Divisor ──
        ctk.CTkFrame(self, fg_color=COR_IEEE_AZUL, height=2, corner_radius=0).pack(fill="x")

        # ── Corpo Principal ──
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=24, pady=20)

        ctk.CTkLabel(corpo, text="📂  Selecione os arquivos", font=("Segoe UI", 13, "bold"), text_color=COR_SUBTEXTO).pack(anchor="w", pady=(0, 8))

        self._sel_planilha = FileSelector(
            corpo,
            label="Planilha de Participantes",
            icone="🗂️",
            tipos=[("Planilha", "*.csv *.xlsx *.xls"), ("CSV", "*.csv"), ("Excel", "*.xlsx *.xls"), ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_planilha.pack(fill="x", pady=(0, 10))

        self._sel_template = FileSelector(
            corpo,
            label="Template do Certificado",
            icone="🖼️",
            tipos=[("Imagem", "*.png *.jpg *.jpeg *.webp"), ("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg"), ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_template.pack(fill="x", pady=(0, 10))

        self._sel_fonte = FileSelector(
            corpo,
            label="Fonte do Texto",
            icone="🔤",
            tipos=[("Arquivos de Fonte", "*.ttf *.otf"), ("TrueType", "*.ttf"), ("OpenType", "*.otf"), ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_fonte.pack(fill="x", pady=(0, 20))

        # ── Configuração de Posicionamento Y ──
        pos_frame = ctk.CTkFrame(corpo, fg_color="transparent")
        pos_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(pos_frame, text="↕️  Posição Vertical do Nome (Pixels):", font=("Segoe UI", 12, "bold"), text_color=COR_TEXTO).pack(side="left")
                    
        self._txt_pos_y = ctk.CTkEntry(pos_frame, width=80, placeholder_text="Ex: 520", fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_pos_y.pack(side="left", padx=15)
        self._txt_pos_y.insert(0, "500")

        # ── Credenciais de Autenticação SMTP ──
        ctk.CTkLabel(corpo, text="🔐  Credenciais de Envio (Gmail)", font=("Segoe UI", 13, "bold"), text_color=COR_SUBTEXTO).pack(anchor="w", pady=(10, 4))

        cred_frame = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, corner_radius=10, border_width=1, border_color=COR_BORDA)
        cred_frame.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(cred_frame, text="E-mail corporativo:", font=("Segoe UI", 12, "bold"), text_color=COR_TEXTO).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self._txt_email = ctk.CTkEntry(cred_frame, placeholder_text="seu.email@ieee.org", fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_email.grid(row=0, column=1, padx=15, pady=12, sticky="ew")

        ctk.CTkLabel(cred_frame, text="Senha de Aplicativo:", font=("Segoe UI", 12, "bold"), text_color=COR_TEXTO).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self._txt_senha = ctk.CTkEntry(cred_frame, placeholder_text="Senha de 16 dígitos do Google", show="*", fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_senha.grid(row=1, column=1, padx=15, pady=12, sticky="ew")

        cred_frame.grid_columnconfigure(1, weight=1)

        # ── Acionamento Primário ──
        self._btn_gerar = ctk.CTkButton(
            corpo,
            text="🎓  GERAR CERTIFICADOS",
            height=56,
            font=("Segoe UI", 15, "bold"),
            fg_color=COR_BOTAO_GERAR,
            hover_color=COR_BOTAO_HOVER,
            corner_radius=12,
            command=self._iniciar_geracao,
        )
        self._btn_gerar.pack(fill="x", pady=(0, 6))

        self._progresso = ctk.CTkProgressBar(corpo, mode="determinate", height=6, corner_radius=3, fg_color=COR_BORDA, progress_color=COR_IEEE_CLARO)
        self._progresso.set(0)
        self._progresso.pack(fill="x", pady=(10, 4))

        # ── Monitoramento ──
        ctk.CTkLabel(corpo, text="📋  Log de execução", font=("Segoe UI", 12, "bold"), text_color=COR_SUBTEXTO).pack(anchor="w", pady=(14, 4))

        self._log = LogBox(corpo)
        self._log.pack(fill="both", expand=True)

        # ── Rodapé Institucional ──
        rodape = ctk.CTkFrame(self, fg_color=COR_PAINEL, corner_radius=0, height=32)
        rodape.pack(fill="x", side="bottom")
        rodape.pack_propagate(False)
        ctk.CTkLabel(rodape, text="IEEE  •  Sistema interno de emissão de certificados", font=("Segoe UI", 9), text_color=COR_SUBTEXTO).pack(expand=True)

        self._log.append("Sistema pronto. Selecione os arquivos e clique em Gerar.", "INFO")

    # ──────────────────────────────────────────────
    #  LÓGICA DE ORQUESTRAÇÃO
    # ──────────────────────────────────────────────
    def _iniciar_geracao(self) -> None:
        """
        Captura os insumos da interface, aplica validações primárias e delega 
        a execução intensiva para uma thread secundária, prevenindo travamentos da UI.
        """
        planilha = self._sel_planilha.caminho
        template = self._sel_template.caminho
        fonte = self._sel_fonte.caminho
        email = self._txt_email.get().strip()
        senha = self._txt_senha.get().strip()

        try:
            pos_y = int(self._txt_pos_y.get().strip())
        except ValueError:
            pos_y = 500

        # Validações estruturais pré-execução
        if not planilha:
            messagebox.showwarning("Atenção", "Selecione a planilha de participantes!")
            return
        if not template:
            messagebox.showwarning("Atenção", "Selecione o template do certificado!")
            return
        if not fonte:
            messagebox.showwarning("Atenção", "Selecione o arquivo de fonte (.ttf ou .otf)!")
            return
        if not email or not senha:
            messagebox.showwarning("Atenção", "Insira as credenciais de e-mail para envio!")
            return

        # Bloqueio de UI durante processamento
        self._btn_gerar.configure(state="disabled", text="⏳  Processando...")
        self._progresso.set(0.0)
        self._progresso.update_idletasks()
        self.update()                    
        
        self._log.limpar()
        self._log.append("═" * 50, "NORMAL")
        self._log.append("   INICIANDO MOTOR DE CERTIFICADOS IEEE", "INFO")
        self._log.append("═" * 50, "NORMAL")

        # Despacho assíncrono para liberar o Main Loop do Tkinter
        t = threading.Thread(
            target=self._executar_geracao,
            args=(planilha, template, fonte, email, senha, pos_y),
            daemon=True,
        )
        t.start()
    
    def atualizar_barra_externa(self, atual: int, total: int) -> None:
        """
        Callback invocado pelo motor principal para renderizar o avanço do processo.
        Utiliza o método 'after' para garantir manipulação segura de threads no Tkinter.
        """
        if total <= 0: 
            total = 1 
            
        porcentagem = float(atual) / float(total)
        
        self.after(0, lambda p=porcentagem: self._progresso.set(p))
        self.after(0, self._progresso.update_idletasks)
        self.after(0, lambda: self._log.append(f"[PROGRESSO] Passo {atual} de {total} ({porcentagem*100:.1f}%)", "INFO"))

    def _executar_geracao(self, planilha: str, template: str, fonte: str, email: str, senha: str, pos_y: int) -> None:
        """
        Ambiente isolado de thread para processamento pesado. 
        Redireciona o stdout para capturar logs do backend e força a limpeza de cache 
        dos módulos para garantir leituras atualizadas a cada nova execução.
        """
        import io
        import contextlib
        import sys

        # Limpeza do cache do interpretador para garantir que execuções consecutivas
        # sem fechamento da interface sempre leiam as configurações mais recentes.
        for mod in ["main", "config_manager", "leitor_csv", "motor_imagem", "exportador", "envio_email", "validador"]:
            sys.modules.pop(mod, None)
        
        try:
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                from main import iniciar_geracao
                from config_manager import bind_salvar_e_gerar
                
                bind_salvar_e_gerar(
                    caminho_planilha=planilha,
                    caminho_template=template,
                    caminho_fonte=fonte,
                    posicao_y=pos_y,
                    iniciar_geracao=iniciar_geracao,
                    callback_progresso=self.atualizar_barra_externa,
                    email_remetente=email,
                    senha_remetente=senha
                )
                
            saida = f.getvalue()
            
            # Classificador de logs em tempo real
            for linha in saida.splitlines():
                if not linha.strip():
                    continue
                if "[ERRO]" in linha or "[FALHA]" in linha:
                    self._log.append(linha, "ERRO")
                elif "[SUCESSO]" in linha:
                    self._log.append(linha, "SUCESSO")
                elif "[INFO]" in linha or "[STATUS]" in linha or "[ASSETS]" in linha:
                    self._log.append(linha, "INFO")
                elif "[AVISO]" in linha:
                    self._log.append(linha, "AVISO")
                else:
                    self._log.append(linha, "NORMAL")
                    
            self._finalizar(sucesso=True)
            self.after(0, lambda: messagebox.showinfo("Sucesso", "Certificados gerados e e-mails enviados!"))
            
        except Exception as e:
            self._log.append(f"[ERRO CRÍTICO] {e}", "ERRO")
            self._finalizar(sucesso=False)
            self.after(0, lambda err=str(e): messagebox.showerror("Erro", err))

    def _finalizar(self, sucesso: bool) -> None:
        """Ponte thread-safe para acionar a restauração da UI."""
        self.after(0, self._restaurar_ui, sucesso)

    def _restaurar_ui(self, sucesso: bool) -> None:
        """Devolve o controle da interface ao usuário após o processamento."""
        if sucesso:
            self._progresso.set(1.0)
        else:
            self._progresso.set(0.0)

        self._btn_gerar.configure(state="normal", text="🎓  GERAR CERTIFICADOS")
        
        if sucesso:
            self._log.append("─" * 50, "NORMAL")
            self._log.append("  ✅  Processo finalizado com sucesso!", "SUCESSO")
            self._log.append("─" * 50, "NORMAL")
        else:
            self._log.append("─" * 50, "NORMAL")
            self._log.append("  ❌  Processo encerrado com erros.", "ERRO")
            self._log.append("─" * 50, "NORMAL")

# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    app = App()
    app.mainloop()