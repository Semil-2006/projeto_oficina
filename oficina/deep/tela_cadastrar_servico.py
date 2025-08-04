import customtkinter as ctk

class TelaCadastrarServico(ctk.CTkFrame):
    def __init__(self, master, salvar_servico_callback, switch_to_servicos):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.salvar_servico_callback = salvar_servico_callback
        self.switch_to_servicos = switch_to_servicos
        
        self.criar_widgets()

    def criar_widgets(self):
        self.label_nome_servico = ctk.CTkLabel(
            self,
            text="Nome do Serviço",
            font=("Century Gothic bold", 18),
            text_color="white"
        )
        self.label_nome_servico.pack(pady=10)

        self.entry_nome_servico = ctk.CTkEntry(
            self,
            placeholder_text="Digite o nome do serviço",
            justify="center",
            border_width=2,
            border_color="gray",
            font=("Century Gothic", 14),
            width=300,
            height=40,
            corner_radius=10
        )
        self.entry_nome_servico.pack(pady=10)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.pack(pady=20)

        self.botao_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="Voltar",
            font=("Arial", 14),
            command=self.switch_to_servicos
        )
        self.botao_voltar.grid(row=0, column=0, padx=10)

        self.botao_cadastrar = ctk.CTkButton(
            self.frame_botoes,
            text="Cadastrar",
            font=("Arial", 14),
            command=self.salvar_servico
        )
        self.botao_cadastrar.grid(row=0, column=1, padx=10)

    def salvar_servico(self):
        nome_servico = self.entry_nome_servico.get().strip()
        self.salvar_servico_callback(nome_servico)