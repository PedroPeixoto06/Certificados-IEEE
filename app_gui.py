import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import threading
import os
import sys

# ── Adiciona a pasta src/ ao path para importar os módulos do projeto ──
if getattr(sys, 'frozen', False):
    DIRETORIO_ATUAL = sys._MEIPASS
    # O diretório onde o .exe está rodando (útil se for salvar arquivos)
    DIRETORIO_EXECUTAVEL = os.path.dirname(sys.executable)
else:
    DIRETORIO_ATUAL = os.path.dirname(os.path.abspath(__file__))
    DIRETORIO_EXECUTAVEL = DIRETORIO_ATUAL

SRC_PATH = os.path.join(DIRETORIO_ATUAL, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# ── Tema e aparência ──
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# ══════════════════════════════════════════════════════════════════════
#  PALETA IEEE  (azul oficial #006699 + grafite escuro)
# ══════════════════════════════════════════════════════════════════════
COR_FUNDO        = "#0D1117"   # fundo da janela
COR_PAINEL       = "#161B22"   # painéis internos
COR_BORDA        = "#1F2937"   # bordas sutis
COR_IEEE_AZUL    = "#006699"   # azul IEEE
COR_IEEE_CLARO   = "#00A0D2"   # azul destaque
COR_TEXTO        = "#E6EDF3"   # texto principal
COR_SUBTEXTO     = "#8B949E"   # texto secundário
COR_SUCESSO      = "#238636"   # verde sucesso
COR_AVISO        = "#E3B341"   # amarelo aviso
COR_ERRO         = "#DA3633"   # vermelho erro
COR_BOTAO_GERAR  = "#0D6EFD"   # azul botão principal
COR_BOTAO_HOVER  = "#0B5ED7"


class LogBox(ctk.CTkFrame):
    """Área de log com scroll, linhas coloridas por tipo."""

    def __init__(self, master, **kwargs):
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

        # tags de cor
        self._text.tag_config("INFO",    foreground=COR_IEEE_CLARO)
        self._text.tag_config("SUCESSO", foreground=COR_SUCESSO)
        self._text.tag_config("ERRO",    foreground=COR_ERRO)
        self._text.tag_config("AVISO",   foreground=COR_AVISO)
        self._text.tag_config("NORMAL",  foreground=COR_TEXTO)

    def append(self, msg: str, tipo: str = "NORMAL"):
        self._text.configure(state="normal")
        self._text.insert("end", msg + "\n", tipo)
        self._text.see("end")
        self._text.configure(state="disabled")

    def limpar(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", "end")
        self._text.configure(state="disabled")


class FileSelector(ctk.CTkFrame):
    """Linha compacta: ícone + label + botão Selecionar."""

    def __init__(self, master, label: str, icone: str,
                 tipos: list, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(fg_color=COR_PAINEL, corner_radius=10,
                       border_width=1, border_color=COR_BORDA)
        self._tipos = tipos
        self._caminho = tk.StringVar(value="Nenhum arquivo selecionado")

        # ── ícone (emoji) ──
        ctk.CTkLabel(self, text=icone, font=("Segoe UI Emoji", 22),
                     fg_color="transparent", text_color=COR_IEEE_CLARO,
                     width=40).pack(side="left", padx=(14, 4), pady=12)

        # ── textos ──
        bloco = ctk.CTkFrame(self, fg_color="transparent")
        bloco.pack(side="left", fill="x", expand=True, padx=4)
        ctk.CTkLabel(bloco, text=label, font=("Segoe UI", 13, "bold"),
                     text_color=COR_TEXTO, anchor="w").pack(anchor="w")
        ctk.CTkLabel(bloco, textvariable=self._caminho,
                     font=("Courier New", 10),
                     text_color=COR_SUBTEXTO, anchor="w",
                     wraplength=340).pack(anchor="w")

        # ── botão ──
        self._btn = ctk.CTkButton(
            self, text="Selecionar",
            width=110, height=36,
            fg_color=COR_IEEE_AZUL, hover_color=COR_IEEE_CLARO,
            font=("Segoe UI", 12, "bold"),
            corner_radius=8,
            command=self._selecionar,
        )
        self._btn.pack(side="right", padx=14, pady=12)

    def _selecionar(self):
        caminho = filedialog.askopenfilename(filetypes=self._tipos)
        if caminho:
            self._caminho.set(caminho)

    @property
    def caminho(self) -> str:
        val = self._caminho.get()
        return "" if val == "Nenhum arquivo selecionado" else val

    def resetar(self):
        self._caminho.set("Nenhum arquivo selecionado")


class App(ctk.CTk):
    def __init__(self):
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
    def _build_ui(self):
        # ── cabeçalho ──
        header = ctk.CTkFrame(self, fg_color=COR_PAINEL,
                              corner_radius=0, height=100)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo_frame = ctk.CTkFrame(header, fg_color="transparent")
        logo_frame.pack(expand=True)

        # ── Logo IEEE a partir do arquivo ──
        logo_path = os.path.join(DIRETORIO_ATUAL, "logo_IEEE.png")
        if os.path.exists(logo_path):
            pil_logo = Image.open(logo_path)
            
            # 1. Garante que o PIL leia o canal de transparência (RGBA)
            pil_logo = pil_logo.convert('RGBA')
            
            # 🚨 PASSO MÁGICO: Remove o fundo branco sólido da imagem original 🚨
            # Pegamos os dados de cada pixel da imagem
            datas = pil_logo.getdata()
            
            newData = []
            # Analisamos pixel por pixel (R, G, B, Alpha)
            for item in datas:
                # Se o pixel for muito branco (R, G e B acima de 240 - permitindo leve variação)
                if item[0] > 240 and item[1] > 240 and item[2] > 240:
                    # Nós o substituímos por um pixel branco totalmente transparente (Alpha = 0)
                    newData.append((255, 255, 255, 0))
                else:
                    # Senão, mantemos o pixel original
                    newData.append(item)
            
            # Gravamos os novos dados vazados de volta na imagem
            pil_logo.putdata(newData)
                
            # 2. Calcula a largura dinamicamente (para não espremer)
            altura_fixa = 60
            largura_orig, altura_orig = pil_logo.size
            proporcao = largura_orig / altura_orig
            largura_calc = int(proporcao * altura_fixa)
            
            ctk_logo = ctk.CTkImage(light_image=pil_logo, dark_image=pil_logo, size=(largura_calc, altura_fixa))
            
            # 🚨 AJUSTE EXTRA: Garante que o background do Label seja transparente 🚨
            logo_label = ctk.CTkLabel(logo_frame, image=ctk_logo, text="", fg_color="transparent")
            logo_label.pack(side="left", padx=(0, 12))
        else:
            ctk.CTkLabel(
                logo_frame,
                text="⬡ IEEE",
                font=("Georgia", 32, "bold"),
                text_color=COR_IEEE_CLARO,
            ).pack(side="left", padx=(0, 12))

        ctk.CTkFrame(logo_frame, fg_color=COR_BORDA,
                     width=2, height=50).pack(side="left", padx=8)

        subtitulo = ctk.CTkFrame(logo_frame, fg_color="transparent")
        subtitulo.pack(side="left")
        ctk.CTkLabel(subtitulo, text="Gerador de Certificados",
                     font=("Segoe UI", 16, "bold"),
                     text_color=COR_TEXTO).pack(anchor="w")
        ctk.CTkLabel(subtitulo, text="Instituto de Engenheiros Eletricistas e Eletrônicos",
                     font=("Segoe UI", 10),
                     text_color=COR_SUBTEXTO).pack(anchor="w")

        # ── divisor ──
        ctk.CTkFrame(self, fg_color=COR_IEEE_AZUL,
                     height=2, corner_radius=0).pack(fill="x")

        # ── corpo ──
        corpo = ctk.CTkFrame(self, fg_color="transparent")
        corpo.pack(fill="both", expand=True, padx=24, pady=20)

        # título da seção
        ctk.CTkLabel(corpo, text="📂  Selecione os arquivos",
                     font=("Segoe UI", 13, "bold"),
                     text_color=COR_SUBTEXTO).pack(anchor="w", pady=(0, 8))

        # seletor planilha
        self._sel_planilha = FileSelector(
            corpo,
            label="Planilha de Participantes",
            icone="🗂️",
            tipos=[("Planilha", "*.csv *.xlsx *.xls"),
                   ("CSV", "*.csv"),
                   ("Excel", "*.xlsx *.xls"),
                   ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_planilha.pack(fill="x", pady=(0, 10))

        # seletor template
        self._sel_template = FileSelector(
            corpo,
            label="Template do Certificado",
            icone="🖼️",
            tipos=[("Imagem", "*.png *.jpg *.jpeg *.webp"),
                   ("PNG", "*.png"),
                   ("JPEG", "*.jpg *.jpeg"),
                   ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_template.pack(fill="x", pady=(0, 10))

        # seletor fonte
        self._sel_fonte = FileSelector(
            corpo,
            label="Fonte do Texto",
            icone="🔤",
            tipos=[("Arquivos de Fonte", "*.ttf *.otf"),
                   ("TrueType", "*.ttf"),
                   ("OpenType", "*.otf"),
                   ("Todos", "*.*")],
            fg_color=COR_PAINEL,
        )
        self._sel_fonte.pack(fill="x", pady=(0, 20))

        # ── Configuração de Posição (Eixo Y) ──
        pos_frame = ctk.CTkFrame(corpo, fg_color="transparent")
        pos_frame.pack(fill="x", pady=(0, 20))

        
        ctk.CTkLabel(pos_frame, text="↕️  Posição Vertical do Nome (Pixels):", 
                     font=("Segoe UI", 12, "bold"), text_color=COR_TEXTO).pack(side="left")
                     
        self._txt_pos_y = ctk.CTkEntry(pos_frame, width=80, placeholder_text="Ex: 520", 
                                       fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_pos_y.pack(side="left", padx=15)
        # Valor padrão para não obrigar a digitar sempre
        self._txt_pos_y.insert(0, "500")

        # ── Seção de Credenciais de E-mail ──
        ctk.CTkLabel(corpo, text="🔐  Credenciais de Envio (Gmail)",
                     font=("Segoe UI", 13, "bold"),
                     text_color=COR_SUBTEXTO).pack(anchor="w", pady=(10, 4))

        cred_frame = ctk.CTkFrame(corpo, fg_color=COR_PAINEL, corner_radius=10,
                                  border_width=1, border_color=COR_BORDA)
        cred_frame.pack(fill="x", pady=(0, 20))

        # Campo de E-mail
        ctk.CTkLabel(cred_frame, text="E-mail corporativo:", font=("Segoe UI", 12, "bold"), 
                     text_color=COR_TEXTO).grid(row=0, column=0, padx=15, pady=12, sticky="w")
        self._txt_email = ctk.CTkEntry(cred_frame, placeholder_text="seu.email@ieee.org",
                                       fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_email.grid(row=0, column=1, padx=15, pady=12, sticky="ew")

        # Campo de Senha (com show="*" para ocultar o que é digitado)
        ctk.CTkLabel(cred_frame, text="Senha de Aplicativo:", font=("Segoe UI", 12, "bold"), 
                     text_color=COR_TEXTO).grid(row=1, column=0, padx=15, pady=12, sticky="w")
        self._txt_senha = ctk.CTkEntry(cred_frame, placeholder_text="Senha de 16 dígitos do Google", show="*",
                                       fg_color=COR_FUNDO, border_color=COR_BORDA, text_color=COR_TEXTO)
        self._txt_senha.grid(row=1, column=1, padx=15, pady=12, sticky="ew")

        cred_frame.grid_columnconfigure(1, weight=1)

        # ── botão principal ──
        self._btn_gerar = ctk.CTkButton(
            corpo,
            text="🎓   GERAR CERTIFICADOS",
            height=56,
            font=("Segoe UI", 15, "bold"),
            fg_color=COR_BOTAO_GERAR,
            hover_color=COR_BOTAO_HOVER,
            corner_radius=12,
            command=self._iniciar_geracao,
        )
        self._btn_gerar.pack(fill="x", pady=(0, 6))

        # barra de progresso (oculta por padrão)
        # barra de progresso (agora sempre visível)
        self._progresso = ctk.CTkProgressBar(
            corpo, mode="determinate",
            height=6, corner_radius=3,
            fg_color=COR_BORDA,
            progress_color=COR_IEEE_CLARO,
        )
        self._progresso.set(0)
        self._progresso.pack(fill="x", pady=(10, 4))

        # ── área de log ──
        ctk.CTkLabel(corpo, text="📋  Log de execução",
                     font=("Segoe UI", 12, "bold"),
                     text_color=COR_SUBTEXTO).pack(anchor="w", pady=(14, 4))

        self._log = LogBox(corpo)
        self._log.pack(fill="both", expand=True)

        # ── rodapé ──
        rodape = ctk.CTkFrame(self, fg_color=COR_PAINEL,
                              corner_radius=0, height=32)
        rodape.pack(fill="x", side="bottom")
        rodape.pack_propagate(False)
        ctk.CTkLabel(rodape,
                     text="IEEE  •  Sistema interno de emissão de certificados",
                     font=("Segoe UI", 9),
                     text_color=COR_SUBTEXTO).pack(expand=True)

        # log inicial
        self._log.append("Sistema pronto. Selecione os arquivos e clique em Gerar.", "INFO")

    # ──────────────────────────────────────────────
    #  LÓGICA DE GERAÇÃO
    # ──────────────────────────────────────────────
    def _iniciar_geracao(self):
        planilha = self._sel_planilha.caminho
        template = self._sel_template.caminho
        fonte = self._sel_fonte.caminho
        email = self._txt_email.get().strip()
        senha = self._txt_senha.get().strip()

        # Pega a posição Y digitada (se der erro, usa 500 como fallback)
        try:
            pos_y = int(self._txt_pos_y.get().strip())
        except ValueError:
            pos_y = 500

        # Travas de segurança
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

        # ── ATIVAÇÃO DA UI E DA BARRA DE PROGRESSO ──
        self._btn_gerar.configure(state="disabled", text="⏳   Processando...")
        self._progresso.set(0.0)
        self._progresso.update_idletasks()
        self.update()                    
        
        self._log.limpar()
        self._log.append("═" * 50, "NORMAL")
        self._log.append("   INICIANDO MOTOR DE CERTIFICADOS IEEE", "INFO")
        self._log.append("═" * 50, "NORMAL")

        # Dispara o processo em segundo plano
        t = threading.Thread(
            target=self._executar_geracao,
            args=(planilha, template, fonte, email, senha, pos_y),
            daemon=True,
        )
        t.start()
    
    def atualizar_barra_externa(self, atual, total):
        # Proteção contra erro matemático
        if total <= 0: 
            total = 1 
            
        porcentagem = float(atual) / float(total)
        
        # 1. Atualiza o valor (p=porcentagem garante que a memória não se perca)
        self.after(0, lambda p=porcentagem: self._progresso.set(p))
        
        # 2. Força o CustomTkinter a desenhar o bloco na tela imediatamente
        self.after(0, self._progresso.update_idletasks)
        
        # 3. Cria um log visual para vermos exatamente o que o motor está enviando
        self.after(0, lambda: self._log.append(f"[PROGRESSO] Passo {atual} de {total} ({porcentagem*100:.1f}%)", "INFO"))

    def _executar_geracao(self, planilha: str, template: str, fonte: str, email: str, senha: str, pos_y: int):
        import io
        import contextlib
        
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

            
    def _finalizar(self, sucesso: bool):
        """Restaura UI após conclusão (chamado da thread de background)."""
        self.after(0, self._restaurar_ui, sucesso)

    def _restaurar_ui(self, sucesso: bool):

        if sucesso:
            self._progresso.set(1.0) # Crava em 100% visualmente
        else:
            self._progresso.set(0.0)

        self._btn_gerar.configure(
            state="normal",
            text="🎓   GERAR CERTIFICADOS"
        )
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
