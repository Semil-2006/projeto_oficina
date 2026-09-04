import customtkinter as ctk
from banco_de_dados_de_servicos import Peca, seccao
from banco_de_dados_clientes import Cliente, secao
from tkinter import messagebox

class TelaEditarPecasUtilizadas(ctk.CTkFrame):
    def __init__(self, master, cliente, switch_to_detalhes_cliente):
        super().__init__(master, fg_color="darkblue")
        self.master = master
        self.cliente = cliente
        self.switch_to_detalhes_cliente = switch_to_detalhes_cliente
        
        # Obter lista de peças utilizadas (se existir)
        self.pecas_utilizadas = cliente.get('pecas_utilizadas', '').split(',') if cliente.get('pecas_utilizadas') else []
        self.pecas_utilizadas_original = self.pecas_utilizadas.copy()  # Guardar estado original para comparação
        
        self.criar_widgets()
        self.configurar_grid()
        self.carregar_pecas()

    def configurar_grid(self):
        # Configuração responsiva do grid
        for i in range(4):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        # Título
        self.titulo = ctk.CTkLabel(
            self,
            text="Selecionar Peças Utilizadas",
            font=('Century Gothic bold', 32),
            text_color="green"
        )
        self.titulo.grid(row=0, column=0, pady=20)

        # Frame para as peças (com scroll)
        self.frame_pecas = ctk.CTkScrollableFrame(self, width=600, height=400)
        self.frame_pecas.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.frame_pecas.grid_columnconfigure(0, weight=1)

        # Botões
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=2, column=0, pady=20)

        self.btn_salvar = ctk.CTkButton(
            self.frame_botoes,
            text="SALVAR",
            font=('Century Gothic bold', 22),
            command=self.salvar_pecas
        )
        self.btn_salvar.grid(row=0, column=0, padx=10)

        self.btn_voltar = ctk.CTkButton(
            self.frame_botoes,
            text="VOLTAR",
            font=('Century Gothic bold', 22),
            command=self.voltar
        )
        self.btn_voltar.grid(row=0, column=1, padx=10)

    def carregar_pecas(self):
        # Buscar todas as peças do banco de dados
        pecas = seccao.query(Peca).all()
        
        # Limpar o frame
        for widget in self.frame_pecas.winfo_children():
            widget.destroy()
        
        # Adicionar cada peça como um botão
        for i, peca in enumerate(pecas):
            # Verificar se a peça está sendo utilizada
            utilizada = peca.nome in self.pecas_utilizadas
            
            # Definir cor do botão
            if utilizada:
                fg_color = "green"
            elif peca.quantidade > 0:
                fg_color = "#2b2b2b"  # Cinza escuro
            else:
                fg_color = "red"
                
            btn = ctk.CTkButton(
                self.frame_pecas,
                text=f"{peca.nome} ({peca.quantidade} disponíveis)",
                font=('Century Gothic bold', 18),
                fg_color=fg_color,
                hover_color=fg_color,
                command=lambda p=peca.nome: self.toggle_peca(p)
            )
            btn.grid(row=i, column=0, pady=5, padx=10, sticky="ew")
            
            # Desabilitar botão se não houver estoque
            if peca.quantidade <= 0 and not utilizada:
                btn.configure(state="disabled")

    def toggle_peca(self, peca_nome):
        # Alternar a presença da peça na lista
        if peca_nome in self.pecas_utilizadas:
            self.pecas_utilizadas.remove(peca_nome)
        else:
            # Verificar se há estoque disponível
            peca_db = seccao.query(Peca).filter_by(nome=peca_nome).first()
            if peca_db and peca_db.quantidade > 0:
                self.pecas_utilizadas.append(peca_nome)
            else:
                messagebox.showerror("Erro", f"Não há estoque disponível de {peca_nome}!")
        
        # Recarregar as peças para atualizar as cores
        self.carregar_pecas()

    def salvar_pecas(self):
        # Atualizar o cliente com as peças selecionadas
        self.cliente['pecas_utilizadas'] = ','.join(self.pecas_utilizadas)
        
        # Atualizar no banco de dados
        cliente_db = secao.query(Cliente).filter_by(id=self.cliente['id']).first()
        if cliente_db:
            # Calcular diferenças para atualizar estoque
            adicionadas = [p for p in self.pecas_utilizadas if p not in self.pecas_utilizadas_original]
            removidas = [p for p in self.pecas_utilizadas_original if p not in self.pecas_utilizadas]
            
            try:
                # Atualizar estoque para peças adicionadas
                for peca_nome in adicionadas:
                    peca_db = seccao.query(Peca).filter_by(nome=peca_nome).first()
                    if peca_db:
                        peca_db.quantidade -= 1
                
                # Atualizar estoque para peças removidas
                for peca_nome in removidas:
                    peca_db = seccao.query(Peca).filter_by(nome=peca_nome).first()
                    if peca_db:
                        peca_db.quantidade += 1
                
                # Atualizar lista de peças no cliente
                cliente_db.pecas_utilizadas = self.cliente['pecas_utilizadas']
                
                # Confirmar todas as alterações
                secao.commit()
                seccao.commit()
                
                messagebox.showinfo("Sucesso", "Peças atualizadas e estoque ajustado!")
            except Exception as e:
                secao.rollback()
                seccao.rollback()
                messagebox.showerror("Erro", f"Falha ao atualizar: {e}")
        else:
            messagebox.showerror("Erro", "Cliente não encontrado no banco de dados!")
        
        # Voltar para a tela de detalhes
        self.switch_to_detalhes_cliente(self.cliente)

    def voltar(self):
        self.switch_to_detalhes_cliente(self.cliente)