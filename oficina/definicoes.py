def limpar_tela(self):
    for widget in self.winfo_children():
        widget.grid_forget()
def mostrar_senhas(self):
    show = "" if self.mostrar_senha.get() else "*"
    self.criar_senha.configure(show=show)
    self.repetir_criar_senha.configure(show=show)
