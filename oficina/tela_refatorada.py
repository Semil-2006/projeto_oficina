import os
import bcrypt
import re
from datetime import datetime
from collections import Counter
from PIL import Image, ImageTk
from tkinter import messagebox, ttk, filedialog, Tk
from tkcalendar import Calendar
import customtkinter as ctk
from fpdf import FPDF
from sqlalchemy import create_engine,Column,Integer,String,Date,Float
from sqlalchemy.orm import sessionmaker, scoped_session

# Configuração do banco de dados
DATABASE_URI = "sqlite:///oficina.db"
engine = create_engine(DATABASE_URI, echo=False)
Session = scoped_session(sessionmaker(bind=engine))

# Models
class BaseModel:
    def save(self):
        session = Session()
        try:
            session.add(self)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            Session.remove()

class Usuario(BaseModel):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    nome_usuario = Column(String(50), unique=True, nullable=False)
    senha = Column(String(60), nullable=False)
    pergunta_seguranca = Column(String(100), nullable=False)
    resposta_seguranca = Column(String(100), nullable=False)

class Cliente(BaseModel):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True)
    email = Column(String(100))
    telefone = Column(String(20))
    data_entrada = Column(Date, nullable=False)
    valor = Column(Float)
    marca_carro = Column(String(50), nullable=False)
    placa_carro = Column(String(10), nullable=False)
    forma_pagamento = Column(String(20))
    data_saida = Column(Date)
    pecas_utilizadas = Column(String(200))

class Peca(BaseModel):
    __tablename__ = 'pecas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)
    quantidade = Column(Integer, default=0, nullable=False)

class Servico(BaseModel):
    __tablename__ = 'servicos'
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False, unique=True)

# Utilitários
class Validadores:
    @staticmethod
    def validar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) != 11:
            return False
        return True

    @staticmethod
    def validar_email(email):
        return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

    @staticmethod
    def validar_telefone(telefone):
        telefone = ''.join(filter(str.isdigit, telefone))
        return len(telefone) >= 10 and len(telefone) <= 11

class Formatadores:
    @staticmethod
    def formatar_telefone(texto):
        texto = ''.join(filter(str.isdigit, texto))
        if texto.startswith("55"):
            texto = texto[2:]
        texto = "55" + texto

        if len(texto) <= 2:
            return f"+{texto}"
        elif len(texto) <= 4:
            return f"+{texto[:2]} ({texto[2:]})"
        elif len(texto) <= 9:
            return f"+{texto[:2]} ({texto[2:4]}) {texto[4:]}"
        else:
            return f"+{texto[:2]} ({texto[2:4]}) {texto[4:9]}-{texto[9:13]}"

    @staticmethod
    def formatar_placa(texto):
        texto = ''.join([char for char in texto if char.isalnum()]).upper()
        if len(texto) > 3:
            texto = texto[:3] + '-' + texto[3:7]
        return texto[:7]

    @staticmethod
    def formatar_cpf(cpf):
        cpf = ''.join(filter(str.isdigit, cpf))
        if len(cpf) > 11:
            cpf = cpf[:11]
        
        if len(cpf) > 9:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
        elif len(cpf) > 6:
            return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
        elif len(cpf) > 3:
            return f"{cpf[:3]}.{cpf[3:]}"
        return cpf

    @staticmethod
    def formatar_valor(valor):
        valor = re.sub(r'\D', '', valor)
        if not valor:
            return "R$ 0,00"
        valor = int(valor)
        return f"R$ {valor // 100},{valor % 100:02d}"

class PDFGenerator:
    @staticmethod
    def gerar_pdf(cliente, caminho_arquivo):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font('Arial', '', 12)
        
        # Cabeçalho
        pdf.set_fill_color(59, 55, 126)
        pdf.rect(0, 0, pdf.w, pdf.h, 'F')
        pdf.set_font('Arial', 'I', 37)
        pdf.set_text_color(255, 255, 255)
        pdf.set_y(10)
        pdf.cell(0, 20, 'Orçamento - PWS DO IRMÃO', border=False, ln=True, align='C')
        pdf.ln(10)
        
        # Logo
        img_path = os.path.join(os.path.dirname(__file__), 'img_do_carro.png')
        if os.path.exists(img_path):
            pdf.image(img_path, x=(pdf.w - 75.7) / 2, y=50, w=75.7, h=39.4)
        
        # Dados do cliente
        pdf.set_y(100)
        pdf.set_fill_color(255, 255, 255)
        pdf.set_text_color(0, 0, 0)
        
        dados = [
            ("NOME", cliente.nome),
            ("CPF", cliente.cpf or "Não informado"),
            ("EMAIL", cliente.email or "Não informado"),
            ("TELEFONE", cliente.telefone or "Não informado"),
            ("MARCA DO CARRO", cliente.marca_carro or "Não informado"),
            ("PLACA DO CARRO", cliente.placa_carro or "Não informado"),
            ("Peças Utilizadas", cliente.pecas_utilizadas or "Não informado"),
            ("Valor Total", f"R${cliente.valor:.2f}" if cliente.valor else "Não informado"),
            ("Forma de Pagamento", cliente.forma_pagamento or "Não informado"),
        ]
        
        for campo, valor in dados:
            pdf.cell(50, 10, campo, border=1, align='L', fill=True)
            pdf.cell(0, 10, valor, border=1, ln=True, align='L')
        
        # Rodapé
        pdf.ln(10)
        pdf.set_font('Arial', 'I', 10)
        pdf.set_text_color(255, 255, 255)
        pdf.multi_cell(0, 10, 'Em caso de dúvidas, não hesite em nos contatar! Estamos à disposição para esclarecer qualquer questão.')
        
        pdf.output(caminho_arquivo)

# Serviços de aplicação
class AuthService:
    @staticmethod
    def cadastrar_usuario(nome_usuario, senha, pergunta_seguranca, resposta_seguranca):
        session = Session()
        try:
            if session.query(Usuario).filter_by(nome_usuario=nome_usuario).first():
                return False, "Usuário já existe"
            
            salt = bcrypt.gensalt()
            hashed = bcrypt.hashpw(senha.encode('utf-8'), salt)
            
            novo_usuario = Usuario(
                nome_usuario=nome_usuario,
                senha=hashed,
                pergunta_seguranca=pergunta_seguranca,
                resposta_seguranca=resposta_seguranca
            )
            session.add(novo_usuario)
            session.commit()
            return True, "Usuário cadastrado com sucesso"
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            Session.remove()

    @staticmethod
    def autenticar_usuario(nome_usuario, senha):
        session = Session()
        try:
            usuario = session.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
            if not usuario:
                return False, "Usuário não encontrado"
            
            if bcrypt.checkpw(senha.encode('utf-8'), usuario.senha):
                return True, "Autenticação bem-sucedida"
            return False, "Senha incorreta"
        except Exception as e:
            return False, str(e)
        finally:
            Session.remove()

    @staticmethod
    def recuperar_senha(nome_usuario, resposta):
        session = Session()
        try:
            usuario = session.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
            if not usuario:
                return False, "Usuário não encontrado"
            
            if usuario.resposta_seguranca.lower() == resposta.lower():
                return True, "Resposta correta"
            return False, "Resposta incorreta"
        except Exception as e:
            return False, str(e)
        finally:
            Session.remove()

class ClienteService:
    @staticmethod
    def criar_cliente(dados):
        session = Session()
        try:
            novo_cliente = Cliente(**dados)
            session.add(novo_cliente)
            session.commit()
            return True, "Cliente cadastrado com sucesso"
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            Session.remove()

    @staticmethod
    def listar_clientes(filtro=None, pagina=0, por_pagina=10):
        session = Session()
        try:
            query = session.query(Cliente)
            if filtro:
                query = query.filter(Cliente.nome.ilike(f"%{filtro}%"))
            
            total = query.count()
            clientes = query.order_by(Cliente.data_entrada.desc()).offset(pagina * por_pagina).limit(por_pagina).all()
            return clientes, total
        except Exception as e:
            return [], 0
        finally:
            Session.remove()

    @staticmethod
    def atualizar_cliente(cliente_id, dados):
        session = Session()
        try:
            cliente = session.query(Cliente).get(cliente_id)
            if not cliente:
                return False, "Cliente não encontrado"
            
            for key, value in dados.items():
                setattr(cliente, key, value)
            
            session.commit()
            return True, "Cliente atualizado com sucesso"
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            Session.remove()

class EstoqueService:
    @staticmethod
    def adicionar_peca(nome, quantidade):
        session = Session()
        try:
            peca = session.query(Peca).filter_by(nome=nome).first()
            if peca:
                peca.quantidade += quantidade
            else:
                nova_peca = Peca(nome=nome, quantidade=quantidade)
                session.add(nova_peca)
            
            session.commit()
            return True, "Peça atualizada com sucesso"
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            Session.remove()

    @staticmethod
    def listar_pecas(filtro=None):
        session = Session()
        try:
            query = session.query(Peca)
            if filtro:
                query = query.filter(Peca.nome.ilike(f"%{filtro}%"))
            return query.all()
        except Exception as e:
            return []
        finally:
            Session.remove()

    @staticmethod
    def atualizar_quantidade(peca_id, nova_quantidade):
        session = Session()
        try:
            peca = session.query(Peca).get(peca_id)
            if peca:
                peca.quantidade = nova_quantidade
                session.commit()
                return True
            return False
        except Exception as e:
            session.rollback()
            return False
        finally:
            Session.remove()

class ServicoService:
    @staticmethod
    def criar_servico(nome):
        session = Session()
        try:
            if session.query(Servico).filter_by(nome=nome).first():
                return False, "Serviço já existe"
            
            novo_servico = Servico(nome=nome)
            session.add(novo_servico)
            session.commit()
            return True, "Serviço cadastrado com sucesso"
        except Exception as e:
            session.rollback()
            return False, str(e)
        finally:
            Session.remove()

    @staticmethod
    def listar_servicos():
        session = Session()
        try:
            return session.query(Servico).all()
        except Exception as e:
            return []
        finally:
            Session.remove()

class RelatorioService:
    @staticmethod
    def relatorio_diario(data):
        session = Session()
        try:
            clientes = session.query(Cliente).filter(Cliente.data_entrada == data).all()
            return clientes
        except Exception as e:
            return []
        finally:
            Session.remove()

    @staticmethod
    def relatorio_mensal(ano, mes):
        session = Session()
        try:
            clientes = session.query(Cliente).filter(
                Cliente.data_entrada.like(f"{ano}-{mes:02d}-%")
            ).all()
            return clientes
        except Exception as e:
            return []
        finally:
            Session.remove()

    @staticmethod
    def relatorio_anual(ano):
        session = Session()
        try:
            clientes = session.query(Cliente).filter(
                Cliente.data_entrada.between(f"{ano}-01-01", f"{ano}-12-31")
            ).all()
            return clientes
        except Exception as e:
            return []
        finally:
            Session.remove()

# Views
class BaseView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="darkblue")
        self.pack(fill="both", expand=True)

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

class LoginView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        # Imagem
        imagem = Image.open("img_do_carro.png").resize((250, 150))
        self.imagem_de_inicio = ImageTk.PhotoImage(imagem)
        lb_imagem = ctk.CTkLabel(self, image=self.imagem_de_inicio, text=None)
        lb_imagem.grid(row=0, column=0, padx=105, pady=(40, 10))

        # Texto de boas-vindas
        texto_boas_vindas = ctk.CTkLabel(self, text="Seja Bem Vindo", 
                                         font=('Century Gothic bold', 32),
                                         text_color="#FF0000")
        texto_boas_vindas.grid(row=1, column=0)

        # Campos de entrada
        self.ver_usuario = ctk.CTkEntry(self, placeholder_text="Usuario", 
                                        justify="center", border_width=3,
                                        border_color="black", 
                                        font=('Century Gothic bold', 20), 
                                        width=250, height=40, corner_radius=45)
        self.ver_usuario.grid(row=2, column=0, pady=(20, 10))

        self.ver_senha = ctk.CTkEntry(self, placeholder_text="Senha", 
                                      justify="center", width=250, height=40,
                                      font=('Century Gothic bold', 20), 
                                      corner_radius=45, border_width=3,
                                      border_color="black", show="*")
        self.ver_senha.grid(row=3, column=0, pady=10)

        # Mostrar senha
        self.mostrar_senha_var = ctk.BooleanVar()
        mostrar_senha_cb = ctk.CTkCheckBox(
            self, text="Mostrar senha", variable=self.mostrar_senha_var,
            command=self.toggle_mostrar_senha,
            font=("Arial", 16), text_color="white", corner_radius=30,
            border_color="black", border_width=3
        )
        mostrar_senha_cb.grid(row=4, column=0, pady=10)

        # Esqueci senha
        esqueci_senha_btn = ctk.CTkButton(self, text="Esqueci minha senha", 
                                          command=self.controller.mostrar_recuperacao_senha,
                                          fg_color="transparent", hover_color="#d1d1d1",
                                          font=("Arial", 16), text_color="blue")
        esqueci_senha_btn.grid(row=5, column=0, pady=10)

        # Botões
        frame_botoes = ctk.CTkFrame(self, fg_color="transparent")
        frame_botoes.grid(row=6, column=0, pady=20)

        btn_entrar = ctk.CTkButton(frame_botoes, text="Entrar", width=120, height=40,
                                   corner_radius=70, font=('Century Gothic bold', 20), 
                                   fg_color="white", text_color="gray", 
                                   command=self.verificar_login)
        btn_entrar.grid(row=0, column=0, padx=10)

        btn_cadastrar = ctk.CTkButton(frame_botoes, text="Cadastrar", width=120, height=40,
                                      corner_radius=70, font=('Century Gothic bold', 20),
                                      command=self.controller.mostrar_cadastro)
        btn_cadastrar.grid(row=0, column=1, padx=10)

    def toggle_mostrar_senha(self):
        show = "" if self.mostrar_senha_var.get() else "*"
        self.ver_senha.configure(show=show)

    def verificar_login(self):
        usuario = self.ver_usuario.get().strip().upper()
        senha = self.ver_senha.get().strip()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        sucesso, mensagem = AuthService.autenticar_usuario(usuario, senha)
        if sucesso:
            self.controller.mostrar_menu_principal()
        else:
            messagebox.showerror("Erro", mensagem)

class CadastroView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        # Título
        titulo = ctk.CTkLabel(self, text="Cadastro", 
                              font=('Century Gothic bold', 42),
                              text_color="green")
        titulo.pack(pady=(40, 10))

        # Divisor
        divisor = ctk.CTkLabel(self, text="-"*50, 
                              font=('Century Gothic bold', 32),
                              text_color="green")
        divisor.pack(pady=(0, 20))

        # Campos de cadastro
        campos_frame = ctk.CTkFrame(self, fg_color="transparent")
        campos_frame.pack(fill="x", padx=50)

        self.criar_usuario = ctk.CTkEntry(campos_frame, placeholder_text="Criar Usuario",
                                          font=('Century Gothic bold', 20),
                                          width=300, height=40, justify="center", 
                                          corner_radius=45, border_width=3,
                                          border_color="black")
        self.criar_usuario.grid(row=0, column=0, pady=10, sticky="ew")

        self.criar_senha = ctk.CTkEntry(campos_frame, placeholder_text="Criar Senha", 
                                        font=('Century Gothic bold', 20),
                                        width=300, height=40, justify="center", 
                                        corner_radius=45, border_width=3,
                                        border_color="black", show="*")
        self.criar_senha.grid(row=1, column=0, pady=10, sticky="ew")

        self.repetir_senha = ctk.CTkEntry(campos_frame, placeholder_text="Repita a Senha", 
                                          font=('Century Gothic bold', 20),
                                          width=300, height=40, justify="center", 
                                          corner_radius=45, border_width=3,
                                          border_color="black", show="*")
        self.repetir_senha.grid(row=2, column=0, pady=10, sticky="ew")

        # Mostrar senha
        self.mostrar_senha_var = ctk.BooleanVar()
        mostrar_senha_cb = ctk.CTkCheckBox(
            campos_frame, text="Mostrar senha", variable=self.mostrar_senha_var,
            command=self.toggle_mostrar_senha,
            font=("Arial", 16), text_color="white", corner_radius=30,
            border_color="black", border_width=3
        )
        mostrar_senha_cb.grid(row=3, column=0, pady=10)

        # Pergunta de segurança
        opcoes = [
            "Qual estado você nasceu?", 
            "Qual é o nome do seu melhor amigo?",
            "Qual o nome do seu primeiro animal?"
        ]
        self.pergunta_seguranca = ctk.CTkComboBox(campos_frame, values=opcoes, 
                                                  width=300, height=40,
                                                  font=("Century Gothic bold", 18), 
                                                  state="readonly")
        self.pergunta_seguranca.grid(row=4, column=0, pady=10, sticky="ew")
        self.pergunta_seguranca.set(opcoes[0])

        self.resposta_seguranca = ctk.CTkEntry(campos_frame, placeholder_text="Resposta", 
                                               font=('Century Gothic bold', 20),
                                               width=300, height=40, justify="center", 
                                               corner_radius=45, border_width=3,
                                               border_color="black")
        self.resposta_seguranca.grid(row=5, column=0, pady=10, sticky="ew")

        # Botões
        botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
        botoes_frame.pack(pady=20)

        btn_criar = ctk.CTkButton(botoes_frame, text="Criar conta", width=150, height=40,
                                  corner_radius=70, font=("Century Gothic bold", 20),
                                  command=self.criar_conta)
        btn_criar.grid(row=0, column=0, padx=10)

        btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", width=150, height=40,
                                   corner_radius=70, font=("Century Gothic bold", 20),
                                   command=self.controller.mostrar_login)
        btn_voltar.grid(row=0, column=1, padx=10)

    def toggle_mostrar_senha(self):
        show = "" if self.mostrar_senha_var.get() else "*"
        self.criar_senha.configure(show=show)
        self.repetir_senha.configure(show=show)

    def criar_conta(self):
        usuario = self.criar_usuario.get().strip().upper()
        senha = self.criar_senha.get().strip()
        repetir_senha = self.repetir_senha.get().strip()
        pergunta = self.pergunta_seguranca.get()
        resposta = self.resposta_seguranca.get().strip()

        # Validações
        if not usuario or not senha or not repetir_senha or not resposta:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return
            
        if senha != repetir_senha:
            messagebox.showerror("Erro", "As senhas não coincidem.")
            return
            
        if len(senha) < 6:
            messagebox.showerror("Erro", "A senha deve ter pelo menos 6 caracteres.")
            return
            
        sucesso, mensagem = AuthService.cadastrar_usuario(
            usuario, senha, pergunta, resposta
        )
        
        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self.controller.mostrar_login()
        else:
            messagebox.showerror("Erro", mensagem)

class RecuperacaoSenhaView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        titulo = ctk.CTkLabel(self, text="Recuperação de Senha", 
                              font=('Century Gothic bold', 32),
                              text_color="green")
        titulo.pack(pady=(40, 20))

        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuário",
                                          font=('Century Gothic bold', 20),
                                          width=300, height=40, justify="center", 
                                          corner_radius=45, border_width=3,
                                          border_color="black")
        self.usuario_entry.pack(pady=10)

        btn_continuar = ctk.CTkButton(self, text="Continuar", width=200, height=40,
                                      corner_radius=70, font=("Century Gothic bold", 20),
                                      command=self.verificar_usuario)
        btn_continuar.pack(pady=20)

        btn_voltar = ctk.CTkButton(self, text="Voltar", width=200, height=40,
                                   corner_radius=70, font=("Century Gothic bold", 20),
                                   command=self.controller.mostrar_login)
        btn_voltar.pack(pady=10)

    def verificar_usuario(self):
        usuario = self.usuario_entry.get().strip().upper()
        session = Session()
        try:
            user = session.query(Usuario).filter_by(nome_usuario=usuario).first()
            if user:
                self.controller.mostrar_pergunta_seguranca(usuario)
            else:
                messagebox.showerror("Erro", "Usuário não encontrado.")
        finally:
            Session.remove()

class PerguntaSegurancaView(BaseView):
    def __init__(self, parent, controller, usuario):
        super().__init__(parent, controller)
        self.usuario = usuario
        self.criar_interface()

    def criar_interface(self):
        session = Session()
        try:
            user = session.query(Usuario).filter_by(nome_usuario=self.usuario).first()
            if not user:
                messagebox.showerror("Erro", "Usuário não encontrado.")
                self.controller.mostrar_login()
                return
                
            titulo = ctk.CTkLabel(self, text="Pergunta de Segurança", 
                                  font=('Century Gothic bold', 32),
                                  text_color="green")
            titulo.pack(pady=(40, 10))

            pergunta_label = ctk.CTkLabel(self, text=user.pergunta_seguranca, 
                                         font=('Century Gothic bold', 20),
                                         text_color="white")
            pergunta_label.pack(pady=10)

            self.resposta_entry = ctk.CTkEntry(self, placeholder_text="Resposta",
                                              font=('Century Gothic bold', 20),
                                              width=300, height=40, justify="center", 
                                              corner_radius=45, border_width=3,
                                              border_color="black")
            self.resposta_entry.pack(pady=20)

            botoes_frame = ctk.CTkFrame(self, fg_color="transparent")
            botoes_frame.pack(pady=20)

            btn_verificar = ctk.CTkButton(botoes_frame, text="Verificar", width=150, height=40,
                                          corner_radius=70, font=("Century Gothic bold", 20),
                                          command=self.verificar_resposta)
            btn_verificar.grid(row=0, column=0, padx=10)

            btn_voltar = ctk.CTkButton(botoes_frame, text="Voltar", width=150, height=40,
                                       corner_radius=70, font=("Century Gothic bold", 20),
                                       command=self.controller.mostrar_recuperacao_senha)
            btn_voltar.grid(row=0, column=1, padx=10)
        finally:
            Session.remove()

    def verificar_resposta(self):
        resposta = self.resposta_entry.get().strip()
        sucesso, mensagem = AuthService.recuperar_senha(self.usuario, resposta)
        
        if sucesso:
            self.controller.mostrar_sucesso_recuperacao()
        else:
            messagebox.showerror("Erro", mensagem)

class SucessoRecuperacaoView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        titulo = ctk.CTkLabel(self, text="Senha Recuperada!", 
                              font=('Century Gothic bold', 32),
                              text_color="green")
        titulo.pack(pady=(100, 20))

        mensagem = ctk.CTkLabel(self, text="Sua senha foi redefinida com sucesso.", 
                               font=('Century Gothic', 20),
                               text_color="white")
        mensagem.pack(pady=10)

        btn_login = ctk.CTkButton(self, text="Voltar ao Login", width=200, height=40,
                                  corner_radius=70, font=("Century Gothic bold", 20),
                                  command=self.controller.mostrar_login)
        btn_login.pack(pady=30)

class MenuPrincipalView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        titulo = ctk.CTkLabel(self, text="Menu Principal", 
                              font=('Century Gothic bold', 32),
                              text_color="yellow")
        titulo.pack(pady=(60, 40))

        # Botões principais
        botoes = [
            ("Clientes", self.controller.mostrar_menu_clientes),
            ("Serviços", self.controller.mostrar_menu_servicos),
            ("Estoque", self.controller.mostrar_menu_estoque),
            ("Relatórios", self.controller.mostrar_menu_relatorios),
            ("Sair", self.controller.sair)
        ]

        for texto, comando in botoes:
            btn = ctk.CTkButton(self, text=texto, width=300, height=50,
                                corner_radius=70, font=("Century Gothic bold", 24),
                                command=comando)
            btn.pack(pady=10)

class ClientesMenuView(BaseView):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)
        self.criar_interface()

    def criar_interface(self):
        titulo = ctk.CTkLabel(self, text="Menu de Clientes", 
                              font=('Century Gothic bold', 32),
                              text_color="yellow")
        titulo.pack(pady=(60, 40))

        # Botões
        botoes = [
            ("Cadastrar Cliente", self.controller.mostrar_cadastro_cliente),
            ("Listar Clientes", self.controller.mostrar_lista_clientes),
            ("Voltar", self.controller.mostrar_menu_principal)
        ]

        for texto, comando in botoes:
            btn = ctk.CTkButton(self, text=texto, width=300, height=50,
                                corner_radius=70, font=("Century Gothic bold", 24),
                                command=comando)
            btn.pack(pady=10)

# ... (outras views seguindo o mesmo padrão)

# Controller principal
class OficinaController:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Oficina Mecânica")
        self.root.geometry("800x600")
        self.root.minsize(800, 600)
        
        # Inicializar sessão
        Session()
        
        # Configurar views
        self.views = {}
        self.carregar_views()
        
        # Mostrar view inicial
        self.mostrar_view("login")
    
    def carregar_views(self):
        container = ctk.CTkFrame(self.root)
        container.pack(fill="both", expand=True)
        
        # Criar todas as views
        self.views["login"] = LoginView(container, self)
        self.views["cadastro"] = CadastroView(container, self)
        self.views["recuperacao_senha"] = RecuperacaoSenhaView(container, self)
        self.views["pergunta_seguranca"] = None  # Será criada dinamicamente
        self.views["sucesso_recuperacao"] = SucessoRecuperacaoView(container, self)
        self.views["menu_principal"] = MenuPrincipalView(container, self)
        self.views["menu_clientes"] = ClientesMenuView(container, self)
        # ... adicionar outras views
        
        # Esconder todas as views inicialmente
        for view in self.views.values():
            if view:
                view.pack_forget()
    
    def mostrar_view(self, view_name, *args):
        # Esconder todas as views
        for view in self.views.values():
            if view:
                view.pack_forget()
        
        # Criar view dinâmica se necessário
        if view_name == "pergunta_seguranca" and args:
            if self.views["pergunta_seguranca"]:
                self.views["pergunta_seguranca"].destroy()
            self.views["pergunta_seguranca"] = PerguntaSegurancaView(
                self.views["login"].master, self, args[0]
            )
        
        # Mostrar a view solicitada
        if view_name in self.views and self.views[view_name]:
            self.views[view_name].pack(fill="both", expand=True)
    
    # Métodos de navegação
    def mostrar_login(self):
        self.mostrar_view("login")
    
    def mostrar_cadastro(self):
        self.mostrar_view("cadastro")
    
    def mostrar_recuperacao_senha(self):
        self.mostrar_view("recuperacao_senha")
    
    def mostrar_pergunta_seguranca(self, usuario):
        self.mostrar_view("pergunta_seguranca", usuario)
    
    def mostrar_sucesso_recuperacao(self):
        self.mostrar_view("sucesso_recuperacao")
    
    def mostrar_menu_principal(self):
        self.mostrar_view("menu_principal")
    
    def mostrar_menu_clientes(self):
        self.mostrar_view("menu_clientes")
    
    # ... outros métodos de navegação
    
    def sair(self):
        Session.remove()
        self.root.destroy()

# Ponto de entrada da aplicação
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    app = OficinaController(root)
    root.mainloop()