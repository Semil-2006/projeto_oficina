import customtkinter as ctk
from tkinter import messagebox

class TelaDetalhesServico(ctk.CTkToplevel):
    def __init__(self, master, servico, deletar_servico_callback, atualizar_lista_callback):
        super().__init__(master)
        self.servico = servico
        self.deletar_servico_callback = deletar_servico_callback
        self.atualizar_lista_callback = atualizar_lista_callback
        
        self.title(f"Detalhes do Serviço: {servico.nome}")
        self.geometry("400x300")
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        
        self.criar_widgets()

    def criar_widgets(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self, fg_color="darkblue")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        label_titulo = ctk.CTkLabel(
            main_frame,
            text=f"Serviço: {self.servico.nome}",
            font=("Century Gothic bold", 20),
            text_color="yellow"
        )
        label_titulo.pack(pady=(20, 30))
        
        # Botão Deletar
        botao_deletar = ctk.CTkButton(
            main_frame,
            text="Deletar Serviço",
            font=("Century Gothic bold", 16),
            width=180,
            height=40,
            fg_color="#B22222",
            hover_color="#CD5C5C",
            command=self.deletar_servico
        )
        botao_deletar.pack(pady=10)
        
        # Botão Voltar
        botao_voltar = ctk.CTkButton(
            main_frame,
            text="Voltar",
            font=("Century Gothic", 14),
            command=self.destroy
        )
        botao_voltar.pack(pady=10)

    def deletar_servico(self):
        if messagebox.askyesno(
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o serviço '{self.servico.nome}'?",
            icon="warning"
        ):
            sucesso = self.deletar_servico_callback(self.servico)
            if sucesso:
                self.atualizar_lista_callback()  # Atualiza a lista na tela principal
                self.destroy()