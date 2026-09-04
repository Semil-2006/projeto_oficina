"""Exemplo de teste de carga com Locust (para a futura camada de API).

A aplicação atual é desktop; este arquivo documenta como estruturar um teste
de carga para uma API REST (roadmap). Uso:

    locust -f loadtest/locustfile.py --host http://localhost:8000

Dependência: pip install locust  (já consta em requirements.txt)
"""
from locust import HttpUser, between, task


class OficinaUser(HttpUser):
    """Usuário simulando chamadas típicas do sistema."""

    wait_time = between(1, 3)

    def on_start(self):
        """Autentica antes de usar a API."""
        resp = self.client.post(
            "/api/auth/login",
            json={"usuario": "gerente", "senha": "senhaForte1"},
        )
        if resp.status_code == 200:
            self.token = resp.json().get("token")
        else:
            self.token = None

    @task(5)
    def listar_clientes(self):
        self.client.get("/api/clientes?pagina=0")

    @task(3)
    def criar_cliente(self):
        self.client.post(
            "/api/clientes",
            json={
                "nome": "Cliente Carga",
                "data_entrada": "2025-01-15",
                "marca_carro": "Volkswagen",
                "placa_carro": "ABC1234",
                "valor": 1500.0,
            },
        )

    @task(2)
    def relatorio_diario(self):
        self.client.get("/api/relatorios/diario?data=2025-01-15")

    @task(1)
    def listar_estoque(self):
        self.client.get("/api/estoque")
