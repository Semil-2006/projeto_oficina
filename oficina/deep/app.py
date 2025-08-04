import customtkinter as ctk
from tela_login import LoginScreen
from tela_clientes import TelaClientes
import bcrypt
from tkinter import messagebox
from banco_de_dados_login import session, Usuario
from tela_cadastrar_cliente import TelaCadastrarCliente
from tela_ver_cliente import TelaVerCliente
from tela_detalhes_cliente import TelaDetalhesCliente
from tela_estoque_menu import EstoqueScreen
from tela_cadastrar_peca import TelaCadastrarPeca
from tela_ver_estoque import TelaVerEstoque
from tela_servicos import ServicosScreen
from tela_cadastrar_servico import TelaCadastrarServico
from tela_listar_servicos import TelaListarServicos
from tela_clientes_servicos import TelaClientesServicos
from banco_de_dados_oficina_servicos import Servico, sessio
from banco_de_dados_de_servicos import Peca, seccao
from banco_de_dados_clientes import Cliente, secao

class Tela(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Oficina")
        self.geometry("450x700")
        self.minsize(450, 700)
        self.resizable(True, True)
        self.configure(fg_color="darkblue")
        
        self.mostrar_tela_login()

    def mostrar_tela_login(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de login
        self.login_screen = LoginScreen(
            self,
            switch_to_register=self.mostrar_tela_cadastro,
            switch_to_forgot_password=self.esqueceu_senha,
            switch_to_main=self.mostrar_tela_menu_principal
        )
        self.login_screen.pack(expand=True, fill="both")

    def mostrar_tela_cadastro(self):
        from tela_cadastro import CadastroScreen
        
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de cadastro
        self.cadastro_screen = CadastroScreen(
            self,
            switch_to_login=self.mostrar_tela_login,
            cadastrar_usuario_callback=self.cadastrar_usuario
        )
        self.cadastro_screen.pack(expand=True, fill="both")

    def mostrar_tela_menu_principal(self):
        from tela_menu_principal import MenuPrincipalScreen

        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela do menu principal
        self.menu_principal = MenuPrincipalScreen(
            self,
            switch_to_clientes=self.mostrar_tela_clientes,  
            switch_to_servicos=self.mostrar_tela_servicos,
            switch_to_estoque=self.mostrar_tela_estoque,
            switch_to_relatorios=self.mostrar_tela_relatorios,
            switch_to_login=self.mostrar_tela_login
        )
        self.menu_principal.pack(expand=True, fill="both")

    def mostrar_tela_detalhes_cliente(self, cliente):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de detalhes do cliente
        self.detalhes_cliente = TelaDetalhesCliente(
            self,
            cliente=cliente,
            switch_to_ver_cliente=self.mostrar_tela_ver_cliente
        )
        self.detalhes_cliente.pack(expand=True, fill="both")

  
    # Adicione este método na classe Tela para a redefinição de senha
    def tela_redefinir_senha(self):
        for widget in self.winfo_children():
            widget.destroy()
        
        self.texto_redefinicao = ctk.CTkLabel(self, text="Redefinir Senha", 
                                            font=('Century Gothic bold', 32),
                                            text_color="green")
        self.texto_redefinicao.grid(pady=(40, 20))

        self.nova_senha = ctk.CTkEntry(self, placeholder_text="Nova Senha", 
                                    font=('Century Gothic bold', 26),
                                    width=250, height=40, justify="center", 
                                    corner_radius=45, border_width=3,
                                    border_color="black", show="*")
        self.nova_senha.grid(pady=10)

        self.confirmar_nova_senha = ctk.CTkEntry(self, placeholder_text="Confirmar Nova Senha", 
                                                font=('Century Gothic bold', 26),
                                                width=250, height=40, justify="center", 
                                                corner_radius=45, border_width=3,
                                                border_color="black", show="*")
        self.confirmar_nova_senha.grid(pady=10)

        self.mostrar_senha = ctk.CTkCheckBox(
            self, text="Mostrar senha", width=250, font=("Arial", 25), 
            text_color="white", corner_radius=30, border_color="black", border_width=3,
            command=lambda: [
                self.nova_senha.configure(show="" if self.mostrar_senha.get() else "*"),
                self.confirmar_nova_senha.configure(show="" if self.mostrar_senha.get() else "*")
            ])
        self.mostrar_senha.grid(pady=10)

        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(pady=20)

        self.botao_redefinir = ctk.CTkButton(self.frame_botoes, text="Redefinir", 
                                            font=("Century Gothic bold", 25),
                                            command=self.redefinir_senha)
        self.botao_redefinir.grid(row=0, column=0, padx=10)

        self.botao_voltar = ctk.CTkButton(self.frame_botoes, text="Voltar", 
                                        font=("Century Gothic bold", 25),
                                        command=self.criar_tela_login)
        self.botao_voltar.grid(row=0, column=1, padx=10)

    # Modifique o método tela_de_sucesso para chamar a tela de redefinição
    def tela_de_sucesso(self):
        self.tela_redefinir_senha()  # Alterado para chamar a redefinição de senha

    # Adicione este método para redefinir a senha
    def redefinir_senha(self):
        nova_senha = self.nova_senha.get().strip()
        confirmar_senha = self.confirmar_nova_senha.get().strip()
        usuario = self.ver_usuario.get().strip().upper()

        if not nova_senha or not confirmar_senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
            
        if nova_senha != confirmar_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
            
        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()
        
        if usuario_encontrado:
            # Criptografa a nova senha
            hashed = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            usuario_encontrado.senha = hashed
            session.commit()
            
            messagebox.showinfo("Sucesso", "Senha redefinida com sucesso!")
            self.criar_tela_login()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    # Modifique o método esqueceu_senha para usar a verificação interna
    def esqueceu_senha(self):
        for widget in self.winfo_children():
            widget.destroy()
        self.texto_de_boas_vindas_esqueci = ctk.CTkLabel(
            self, text="Vamos recuperar sua senha!",
            font=('Century Gothic bold',22), text_color="green")
        self.texto_de_boas_vindas_esqueci.grid(pady=(260,20))
        
        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", justify="center",border_width=3,
                                        border_color="black",font=('Century Gothic bold',32), width=250,height=40,
                                        corner_radius=45)
        self.ver_usuario.grid(padx=75)
        
        self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_botoes.grid(row=6, column=0, pady=10)
        
        self.botao_voltar = ctk.CTkButton(self.frame_botoes, command=self.mostrar_tela_login, text="Voltar")
        self.botao_voltar.grid(padx=8,row=0, column=0)
        
        self.botao_continuar = ctk.CTkButton(
            self.frame_botoes,
            text="Continuar",
            command=self.verificar_usuario_para_recuperacao  # Alterado para método interno
        )
        self.botao_continuar.grid(padx=8, row=0, column=1)
        
        self.frame_botoes.grid_columnconfigure(0, weight=1)
        self.frame_botoes.grid_columnconfigure(1, weight=1)

    # Adicione este método para verificar o usuário
    def verificar_usuario_para_recuperacao(self):
        usuario = self.ver_usuario.get().strip().upper()
        
        if not usuario:
            messagebox.showerror("Erro", "Por favor, insira um nome de usuário.")
            return
            
        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()
        
        if usuario_encontrado:
            self.tela_de_pergunta()
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    # Modifique o método tela_de_pergunta para usar a verificação interna
    def tela_de_pergunta(self):
        for widget in self.winfo_children():
            widget.destroy()
        usuario = self.ver_usuario.get().strip().upper()
        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()

        if usuario_encontrado:
            pergunta = usuario_encontrado.pergunta_seguranca
            self.texto_pergunta = ctk.CTkLabel(self, text=f"Pergunta: {pergunta}",
                                            font=('Century Gothic bold', 18), text_color="blue")
            self.texto_pergunta.grid(row=0, column=0, padx=20, pady=(50, 20), columnspan=2)

            self.resposta = ctk.CTkEntry(self, placeholder_text="Resposta", justify="center", border_width=2,
                                        border_color="black", font=('Century Gothic bold', 24), width=250, height=40,
                                        corner_radius=45)
            self.resposta.grid(row=1, column=0, columnspan=2, padx=50, pady=15)

            self.frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
            self.frame_botoes.grid(row=2, column=0, columnspan=2, pady=30)

            self.botao_voltar = ctk.CTkButton(self.frame_botoes, command=self.criar_tela_login, text="Voltar", width=120)
            self.botao_voltar.grid(row=0, column=0, padx=8, pady=10)

            self.botao_continuar = ctk.CTkButton(
                self.frame_botoes,
                text="Confirmar",
                command=self.verificar_resposta  # Alterado para método interno
            )
            self.botao_continuar.grid(row=0, column=1, padx=8, pady=10)

            self.frame_botoes.grid_columnconfigure(0, weight=1)
            self.frame_botoes.grid_columnconfigure(1, weight=1)
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

    # Adicione este método para verificar a resposta
    def verificar_resposta(self):
        usuario = self.ver_usuario.get().strip().upper()
        resposta = self.resposta.get().strip()
        
        if not usuario or not resposta:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
            
        usuario_encontrado = session.query(Usuario).filter_by(nome_usuario=usuario).first()
        
        if usuario_encontrado:
            # Verifica a resposta (sem hash para simplicidade)
            if resposta == usuario_encontrado.resposta_seguranca:
                self.tela_de_sucesso()  # Chama a tela de redefinição
            else:
                messagebox.showerror("Erro", "Resposta de segurança incorreta.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")
    
    def mostrar_tela_cadastrar_cliente(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de cadastro de cliente
        self.cadastro_cliente = TelaCadastrarCliente(
            self,
            switch_to_clientes=self.mostrar_tela_menu_principal
        )
        self.cadastro_cliente.pack(expand=True, fill="both")
    
    def mostrar_tela_clientes(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de clientes (menu)
        self.clientes_screen = TelaClientes(
            self,
            switch_to_cadastrar_cliente=self.mostrar_tela_cadastrar_cliente,
            switch_to_ver_cliente=self.mostrar_tela_ver_cliente,
            switch_to_menu_principal=self.mostrar_tela_menu_principal
        )
        self.clientes_screen.pack(expand=True, fill="both")
    
    def mostrar_tela_ver_cliente(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de visualização de clientes
        self.ver_clientes_screen = TelaVerCliente(
            self,
            switch_to_clientes=self.mostrar_tela_clientes,
            switch_to_detalhes_cliente=self.mostrar_tela_detalhes_cliente
        )
        self.ver_clientes_screen.pack(expand=True, fill="both")
    
    def mostrar_tela_servicos(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de serviços (menu)
        self.servicos_screen = ServicosScreen(
            self,
            switch_to_cadastrar_servico=self.mostrar_tela_cadastrar_servico,
            switch_to_listar_servicos=self.mostrar_tela_listar_servicos,
            switch_to_menu_principal=self.mostrar_tela_menu_principal
        )
        self.servicos_screen.pack(expand=True, fill="both")
    
    def mostrar_tela_cadastrar_servico(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de cadastro de serviço
        self.cadastrar_servico_screen = TelaCadastrarServico(
            self,
            salvar_servico_callback=self.salvar_servico,
            switch_to_servicos=self.mostrar_tela_servicos
        )
        self.cadastrar_servico_screen.pack(expand=True, fill="both")
    
    def mostrar_tela_listar_servicos(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de listar serviços
        self.listar_servicos_screen = TelaListarServicos(
            self,
            carregar_servicos_callback=self.carregar_servicos,
            switch_to_servicos=self.mostrar_tela_servicos,
            deletar_servico_callback=self.deletar_servico
        )
        self.listar_servicos_screen.pack(expand=True, fill="both")

    def mostrar_tela_clientes_servicos(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de clientes/serviços
        self.clientes_servicos_screen = TelaClientesServicos(
            self,
            carregar_clientes_servicos_callback=self.carregar_clientes_servicos,
            editar_cliente_callback=self.mostrar_tela_editar_cliente_servico,
            switch_to_servicos=self.mostrar_tela_servicos
        )
        self.clientes_servicos_screen.pack(expand=True, fill="both")
    
    # Métodos auxiliares para serviços
    def salvar_servico(self, nome_servico):
        if not nome_servico:
            messagebox.showerror("Erro", "O nome do serviço não pode estar vazio.")
            return

        try:
            novo_servico = Servico(nome=nome_servico)
            sessio.add(novo_servico)
            sessio.commit()
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
            self.mostrar_tela_servicos()
        except Exception as e:
            sessio.rollback()
            messagebox.showerror("Erro", f"Erro ao cadastrar serviço: {e}")

    def deletar_servico(self, servico):
        try:
            sessio.delete(servico)
            sessio.commit()
            messagebox.showinfo("Sucesso", f"Serviço '{servico.nome}' excluído com sucesso!")
            return True
        except Exception as e:
            sessio.rollback()
            messagebox.showerror("Erro", f"Erro ao excluir serviço: {str(e)}")
            return False
    
    def carregar_servicos(self):
        return sessio.query(Servico).all()
    
    def carregar_clientes_servicos(self):
        return secao.query(Cliente).all()
    
    def mostrar_tela_editar_cliente_servico(self, cliente_nome):
        # Implementar a tela de edição do cliente (já existente em outro módulo)
        # Por enquanto, vamos apenas mostrar uma mensagem
        messagebox.showinfo("Editar", f"Editar cliente: {cliente_nome}")
        # Você pode reutilizar a tela de edição que já foi criada para a parte de clientes
        # Se já tiver, chame o método correspondente passando o cliente
    
    # Tela de estoque (menu)
    def mostrar_tela_estoque(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de estoque (menu)
        self.estoque_screen = EstoqueScreen(
            self,
            switch_to_adicionar_pecas=self.mostrar_tela_adicionar_pecas,
            switch_to_ver_estoque=self.mostrar_tela_ver_estoque,
            switch_to_menu_principal=self.mostrar_tela_menu_principal
        )
        self.estoque_screen.pack(expand=True, fill="both")
    
    # Tela para adicionar peças
    def mostrar_tela_adicionar_pecas(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de cadastro de peça
        self.tela_cadastrar_peca = TelaCadastrarPeca(
            self,
            switch_to_estoque=self.mostrar_tela_estoque
        )
        self.tela_cadastrar_peca.pack(expand=True, fill="both")
    
    # Tela para ver o estoque
    def mostrar_tela_ver_estoque(self):
        # Remove qualquer tela existente
        for widget in self.winfo_children():
            widget.destroy()
        
        # Cria a tela de visualização de estoque
        self.tela_ver_estoque = TelaVerEstoque(
            self,
            switch_to_estoque=self.mostrar_tela_estoque
        )
        self.tela_ver_estoque.pack(expand=True, fill="both")
    
    # Tela de relatórios (a ser implementada)
    def mostrar_tela_relatorios(self):
        pass
    
    def cadastrar_usuario(self, usuario_entry, senha_entry, repetir_senha_entry, pergunta_combo, resposta_entry, callback_sucesso):
        usuario = usuario_entry.get().strip().upper()
        senha = senha_entry.get().strip()
        repetir_senha = repetir_senha_entry.get().strip()
        pergunta = pergunta_combo.get()
        resposta = resposta_entry.get().strip()

        if not usuario:
            messagebox.showerror("Erro", "O campo usuário é obrigatório!")
            return
            
        if not senha:
            messagebox.showerror("Erro", "O campo senha é obrigatório!")
            return
            
        if senha != repetir_senha:
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
            
        if not pergunta or pergunta == "Qual estado você nasceu?":
            messagebox.showerror("Erro", "Selecione uma pergunta de segurança válida!")
            return
            
        if not resposta:
            messagebox.showerror("Erro", "O campo resposta é obrigatório!")
            return

        usuario_existente = session.query(Usuario).filter_by(nome_usuario=usuario).first()
        if usuario_existente:
            messagebox.showerror("Erro", "Usuário já existe!")
            return

        try:
            salt = bcrypt.gensalt()
            senha_hash = bcrypt.hashpw(senha.encode('utf-8'), salt)
            
            novo_usuario = Usuario(
                nome_usuario=usuario,
                senha=senha_hash,
                pergunta_seguranca=pergunta,
                resposta_seguranca=resposta
            )
            
            session.add(novo_usuario)
            session.commit()
            
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
            callback_sucesso()
            
        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro", f"Erro ao cadastrar usuário: {str(e)}")


if __name__ == "__main__":
    app = Tela()
    app.mainloop()