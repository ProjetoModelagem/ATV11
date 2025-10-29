from locust import HttpUser, task, between

class UsuarioEcommerce(HttpUser):
    wait_time = between(1, 3)  # think time humano

    @task(5)
    def ver_home(self):
        with self.client.get("/", name="GET /", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("home falhou")

    @task(3)
    def buscar_produto(self):
        with self.client.get("/api/produtos?q=tv", name="GET /api/produtos", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("busca falhou")

    @task(1)
    def adicionar_carrinho(self):
        with self.client.post("/api/carrinho", json={"sku": "TV123", "qty": 1}, name="POST /api/carrinho", catch_response=True) as resp:
            if resp.status_code != 200:
                resp.failure("carrinho falhou")
