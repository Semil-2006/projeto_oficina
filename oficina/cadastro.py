import re
import customtkinter as ctk
from tkinter import messagebox
from dados_login import Usuario, get_session
from passlib.context import CryptContext
from tela import Tela

# Contexto de hashing (como padrão, usamos bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TelaCadastro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cadastro de Usuário")
        self.geometry("600x600")
        self.configure(fg_color="darkblue")

        # Widgets
        self.lbl_titulo = ctk.CTkLabel(self, text="Cadastro de Usuário", font=('Century Gothic', 24, 'bold'), text_color="white")
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, pady=10)

        self.texto = ctk.CTkLabel(self, text="--"*9, font=('Century Gothic', 32, 'bold'), text_color="green")
        self.texto.grid(row=1, column=0, columnspan=2, pady=10)

        self.entry_usuario = ctk.CTkEntry(self, placeholder_text="Nome de usuário", width=300, height=40, font=('Century Gothic', 16))
        self.entry_usuario.grid(row=3, column=0, columnspan=2, pady=5)

        self.entry_senha = ctk.CTkEntry(self, placeholder_text="Senha", show="*", width=300, height=40, font=('Century Gothic', 16))
        self.entry_senha.grid(row=4, column=0, columnspan=2, pady=5)

        self.entry_senha2 = ctk.CTkEntry(self, placeholder_text="Repita a senha", show="*", width=300, height=40, font=('Century Gothic', 16))
        self.entry_senha2.grid(row=5, column=0, columnspan=2, pady=5)

        # Checkbox para mostrar as senhas
        self.chk_mostrar = ctk.CTkCheckBox(self, text="Mostrar senhas", command=self._toggle_senha)
        self.chk_mostrar.grid(row=6, column=0, columnspan=2, pady=10)

        self.perguntas = [
            "Qual estado você nasceu?",
            "Qual é o nome do seu melhor amigo?",
            "Qual o nome do seu primeiro animal?"
        ]
        self.combo_pergunta = ctk.CTkComboBox(self, values=self.perguntas, width=300, height=38, font=('Century Gothic', 16), state="readonly")
        self.combo_pergunta.grid(row=7, column=0, columnspan=2, pady=5)

        self.entry_resposta = ctk.CTkEntry(self, placeholder_text="Resposta de segurança", width=300, height=40, font=('Century Gothic', 16))
        self.entry_resposta.grid(row=8, column=0, columnspan=2, pady=5)

        self.btn_confirmar = ctk.CTkButton(self, text="Confirmar", command=self._on_confirmar, width=140, font=('Century Gothic', 16))
        self.btn_confirmar.grid(row=9, column=0, columnspan=2, pady=20)

        # Ajustes de redimensionamento
        for i in range(10):
            self.grid_rowconfigure(i, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def _toggle_senha(self):
        show = "" if self.chk_mostrar.get() else "*"
        self.entry_senha.configure(show=show)
        self.entry_senha2.configure(show=show)

    def _on_confirmar(self):
        nome = self.entry_usuario.get().strip()
        senha = self.entry_senha.get()
        senha2 = self.entry_senha2.get()
        pergunta = self.combo_pergunta.get()
        resposta = self.entry_resposta.get().strip()

        # Validações de entrada
        if not nome or not senha or not senha2 or not pergunta or not resposta:
            messagebox.showerror("Erro", "Todos os campos são obrigatórios.")
            return
        if senha != senha2:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
        if len(senha) < 4:
            messagebox.showerror("Erro", "A senha deve ter ao menos 6 caracteres.")
            return
        if not re.match(r'^[A-Za-z0-9_]+$', nome):
            messagebox.showerror("Erro", "Usuário só pode conter letras, números e underscore.")
            return

        # Criptografando a senha
        senha_hash = pwd_context.hash(senha)

        session = get_session()
        try:
            # Melhorando a consulta para verificar a existência do usuário
            existe = session.query(Usuario).filter_by(nome_usuario=nome).first()
            if existe:
                messagebox.showerror("Erro", "Este usuário já existe.")
                return

            # Criando o novo usuário com os dados criptografados
            novo = Usuario(
                nome_usuario=nome,
                senha=senha_hash,
                pergunta_seguranca=pergunta,
                resposta_seguranca=resposta
            )

            session.add(novo)
            session.commit()

            messagebox.showinfo("Sucesso", f"Usuário '{nome}' criado com sucesso!")
            self.destroy()  # Fecha a tela atual de cadastro
            nova_tela = Tela()  # Cria a nova tela
            nova_tela.mainloop()  # Inicia a nova tela
            
            

        except Exception as e:
            session.rollback()
            messagebox.showerror("Erro ao salvar", f"Erro ao salvar os dados: {e}")
        finally:
            session.close()

if __name__ == "__main__":
    tela = TelaCadastro()
    tela.mainloop()
