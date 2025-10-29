from locust import HttpUser, task, constant

class UsuarioStress(HttpUser):
    wait_time = constant(0.2)  # quase sem "think time", é ataque pesado

    @task
    def checkout(self):
        # caminho crítico de negócio
        self.client.post(
            "/api/checkout",
            json={"sku": "TV123", "qty": 1, "payment": "card"},
            name="POST /api/checkout"
        )
