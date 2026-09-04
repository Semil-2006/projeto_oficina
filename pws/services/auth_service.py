"""Serviço de autenticação: hash, cadastro, login e recuperação de senha.

Corrige a vulnerabilidade da versão original que armazenava a resposta de
segurança em texto puro e a comparava sem hashing.
"""
from __future__ import annotations

import bcrypt

from pws.models import Usuario

PERGUNTAS_SEGURANCA = [
    "Qual estado você nasceu?",
    "Qual é o nome do seu melhor amigo?",
    "Qual o nome do seu primeiro animal?",
]


def hash_senha(senha_plana: str) -> bytes:
    """Gera o hash bcrypt de uma senha em texto puro."""
    return bcrypt.hashpw(senha_plana.encode("utf-8"), bcrypt.gensalt())


def verificar_senha(senha_plana: str, hash_armazenado) -> bool:
    """Compara uma senha em texto puro com um hash bcrypt."""
    if isinstance(hash_armazenado, str):
        hash_armazenado = hash_armazenado.encode("utf-8")
    return bcrypt.checkpw(senha_plana.encode("utf-8"), hash_armazenado)


class UsuarioJaExisteError(Exception):
    """Lançada quando o nome de usuário já está cadastrado."""


class CredenciaisInvalidasError(Exception):
    """Lançada quando usuário ou senha são inválidos."""


class UsuarioNaoEncontradoError(Exception):
    """Lançada quando o usuário não existe."""


class RespostaIncorretaError(Exception):
    """Lançada quando a resposta de segurança está incorreta."""


class AuthService:
    """Operações de conta do sistema."""

    PASSWORD_MIN_LENGTH = 4

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def cadastrar_usuario(
        self,
        nome_usuario: str,
        senha: str,
        pergunta_seguranca: str,
        resposta_seguranca: str,
    ) -> Usuario:
        """Cadastra um novo usuário, validando entradas e unicidade.

        Retorna o usuário criado. Lança exceções de validação em caso de erro.
        """
        nome_usuario = (nome_usuario or "").strip().upper()
        if not nome_usuario:
            raise ValueError("O campo 'Usuário' deve ser preenchido.")
        if not senha:
            raise ValueError("O campo 'Senha' deve ser preenchido.")
        if len(senha) < self.PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"A senha deve ter pelo menos {self.PASSWORD_MIN_LENGTH} caracteres."
            )
        if not pergunta_seguranca:
            raise ValueError("Selecione uma pergunta de segurança.")
        if not resposta_seguranca:
            raise ValueError("O campo 'Resposta' deve ser preenchido.")

        session = self.session_factory()
        try:
            existente = (
                session.query(Usuario)
                .filter_by(nome_usuario=nome_usuario)
                .first()
            )
            if existente:
                raise UsuarioJaExisteError(
                    "Nome de usuário já cadastrado. Escolha outro."
                )

            novo = Usuario(
                nome_usuario=nome_usuario,
                senha=senha,
                pergunta_seguranca=pergunta_seguranca.strip(),
                resposta_seguranca=resposta_seguranca.strip().upper(),
            )
            session.add(novo)
            session.commit()
            session.refresh(novo)
            return novo
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()

    def autenticar(self, nome_usuario: str, senha: str) -> Usuario:
        """Autentica um usuário. Retorna o usuário ou lança exceção."""
        nome_usuario = (nome_usuario or "").strip().upper()
        if not nome_usuario or not senha:
            raise CredenciaisInvalidasError("Todos os campos devem ser preenchidos.")

        session = self.session_factory()
        try:
            usuario = (
                session.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
            )
            if not usuario:
                raise CredenciaisInvalidasError("Usuário não existe.")
            if not usuario.verificar_senha(senha):
                raise CredenciaisInvalidasError("Senha incorreta. Tente novamente.")
            return usuario
        finally:
            self.session_factory.remove()

    def buscar_usuario(self, nome_usuario: str) -> Usuario | None:
        """Busca um usuário pelo nome de usuário (sem levantar exceção)."""
        session = self.session_factory()
        try:
            return (
                session.query(Usuario)
                .filter_by(nome_usuario=(nome_usuario or "").strip().upper())
                .first()
            )
        finally:
            self.session_factory.remove()

    def verificar_existe(self, nome_usuario: str) -> bool:
        """Verifica se um usuário existe."""
        return self.buscar_usuario(nome_usuario) is not None

    def verificar_resposta(self, nome_usuario: str, resposta: str) -> bool:
        """Valida a resposta de segurança de um usuário."""
        session = self.session_factory()
        try:
            usuario = (
                session.query(Usuario)
                .filter_by(nome_usuario=(nome_usuario or "").strip().upper())
                .first()
            )
            if not usuario:
                raise UsuarioNaoEncontradoError("Usuário não encontrado.")
            if not resposta:
                raise ValueError("O campo 'Resposta' deve ser preenchido.")
            return usuario.verificar_resposta(resposta.strip().upper())
        finally:
            self.session_factory.remove()

    def redefinir_senha(self, nome_usuario: str, nova_senha: str) -> None:
        """Redefine a senha de um usuário (após validar a resposta)."""
        nome_usuario = (nome_usuario or "").strip().upper()
        if not nova_senha:
            raise ValueError("A nova senha não pode ser vazia.")
        if len(nova_senha) < self.PASSWORD_MIN_LENGTH:
            raise ValueError(
                f"A senha deve ter pelo menos {self.PASSWORD_MIN_LENGTH} caracteres."
            )

        session = self.session_factory()
        try:
            usuario = (
                session.query(Usuario).filter_by(nome_usuario=nome_usuario).first()
            )
            if not usuario:
                raise UsuarioNaoEncontradoError("Usuário não encontrado.")
            usuario.senha = nova_senha
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            self.session_factory.remove()
