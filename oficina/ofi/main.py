from cadastro import TelaCadastro

def abrir_cadastro(self):
    self._configurar_tela(), etc.
    tela = TelaCadastro(voltar_callback=self.criar_tela_login)
    tela.mainloop()
